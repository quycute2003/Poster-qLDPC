#!/usr/bin/env python3
"""Build the editable qLDPC poster from its Office Open XML source.

Python 3.9+; no pip dependencies. PDF requires LibreOffice; PNG requires
pdftoppm (Poppler). All input paths are relative to this project directory.
"""
import argparse
import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def q(prefix, name):
    return '{' + NS[prefix] + '}' + name


def text_of(node):
    return '\n'.join(
        ''.join(t.text or '' for t in p.findall('.//a:t', NS))
        for p in node.findall('p:txBody/a:p', NS)
    )


def set_attribute(node, key, value):
    value = str(value)
    if node.get(key) == value:
        return False
    node.set(key, value)
    return True


def replace_text(node, value):
    """Keep paragraph styling; leave rich math runs intact when text is unchanged."""
    if text_of(node) == value:
        return False
    body = node.find('p:txBody', NS)
    if body is None:
        raise ValueError('text can only be edited on a text shape')
    original = body.findall('a:p', NS)
    for p in original:
        body.remove(p)
    for i, line in enumerate(value.split('\n')):
        new = ET.SubElement(body, q('a', 'p'))
        template = original[min(i, len(original) - 1)] if original else None
        if template is not None:
            pr = template.find('a:pPr', NS)
            if pr is not None:
                new.append(copy.deepcopy(pr))
        run = ET.SubElement(new, q('a', 'r'))
        if template is not None:
            pr = template.find('a:r/a:rPr', NS)
            if pr is not None:
                run.append(copy.deepcopy(pr))
        ET.SubElement(run, q('a', 't')).text = line
    return True


def set_rgb(parent, color):
    color = color.lstrip('#').upper()
    if not re.fullmatch('[0-9A-F]{6}', color):
        raise ValueError('RGB colors must use six hexadecimal digits')
    rgb = parent.find('a:srgbClr', NS)
    if rgb is not None and rgb.get('val') == color and len(parent) == 1:
        return False
    for child in list(parent):
        parent.remove(child)
    ET.SubElement(parent, q('a', 'srgbClr'), {'val': color})
    return True


def apply_config(parts, config):
    slide_path = 'ppt/slides/slide1.xml'
    slide = ET.fromstring(parts[slide_path])
    tree = slide.find('p:cSld/p:spTree', NS)
    nodes = {}
    for node in tree:
        identity = node.find('.//p:cNvPr', NS)
        if identity is not None:
            nodes[identity.get('id')] = node
    canvas = config['canvas']
    sx = round(canvas['width_cm'] * 360000) / canvas['design_width']
    sy = round(canvas['height_cm'] * 360000) / canvas['design_height']
    changed = False
    for key, spec in config['objects'].items():
        node = nodes.get(str(spec['shape_id']))
        if node is None:
            raise ValueError('Unknown shape in config: ' + key)
        if 'text' in spec:
            changed |= replace_text(node, spec['text'])
        if 'position' in spec:
            xf = node.find('p:spPr/a:xfrm', NS)
            if xf is None:
                xf = node.find('p:xfrm', NS)
            if xf is None:
                raise ValueError('Shape has no position: ' + key)
            off, ext = xf.find('a:off', NS), xf.find('a:ext', NS)
            pos = spec['position']
            for tag, attr, field, scale in [
                (off, 'x', 'x', sx), (off, 'y', 'y', sy),
                (ext, 'cx', 'width', sx), (ext, 'cy', 'height', sy),
            ]:
                changed |= set_attribute(tag, attr, round(pos[field] * scale))
        if 'alignment' in spec:
            align = {'left': 'l', 'center': 'ctr', 'right': 'r', 'justify': 'just', 'distributed': 'dist'}[spec['alignment']]
            for para in node.findall('p:txBody/a:p', NS):
                pr = para.find('a:pPr', NS)
                if pr is None:
                    pr = ET.Element(q('a', 'pPr')); para.insert(0, pr)
                    changed = True
                if pr.get('algn', 'l') != align:
                    changed |= set_attribute(pr, 'algn', align)
        if 'font_size_pt' in spec:
            for para in node.findall('p:txBody/a:p', NS):
                pr = para.find('a:pPr', NS)
                if pr is None:
                    pr = ET.Element(q('a', 'pPr')); para.insert(0, pr)
                default = pr.find('a:defRPr', NS)
                if default is None:
                    default = ET.SubElement(pr, q('a', 'defRPr'))
                changed |= set_attribute(default, 'sz', round(spec['font_size_pt'] * 100))
                for run in para.findall('a:r', NS):
                    rp = run.find('a:rPr', NS)
                    if rp is None:
                        rp = ET.Element(q('a', 'rPr')); run.insert(0, rp)
                    changed |= set_attribute(rp, 'sz', round(spec['font_size_pt'] * 100))
        if 'color' in spec:
            for para in node.findall('p:txBody/a:p', NS):
                pr = para.find('a:pPr', NS)
                if pr is None:
                    pr = ET.Element(q('a', 'pPr')); para.insert(0, pr)
                default = pr.find('a:defRPr', NS)
                if default is None:
                    default = ET.SubElement(pr, q('a', 'defRPr'))
                fills = []
                for target in [default] + para.findall('a:r/a:rPr', NS):
                    fill = target.find('a:solidFill', NS)
                    if fill is None:
                        fill = ET.SubElement(target, q('a', 'solidFill'))
                    fills.append(fill)
                for fill in fills:
                    changed |= set_rgb(fill, spec['color'])
    if changed:
        parts[slide_path] = ET.tostring(slide, encoding='UTF-8', xml_declaration=True)
    pres = ET.fromstring(parts['ppt/presentation.xml'])
    size = pres.find('p:sldSz', NS)
    resized = set_attribute(size, 'cx', round(canvas['width_cm'] * 360000))
    resized |= set_attribute(size, 'cy', round(canvas['height_cm'] * 360000))
    if resized:
        parts['ppt/presentation.xml'] = ET.tostring(pres, encoding='UTF-8', xml_declaration=True)
    return parts


def find_executable(explicit, name):
    if explicit:
        candidate = Path(explicit).expanduser()
        if candidate.is_file():
            return str(candidate.resolve())
        found = shutil.which(explicit)
        if found:
            return found
        raise FileNotFoundError(explicit)
    found = shutil.which(name)
    if found:
        return found
    if name == 'soffice':
        candidates = [Path('/Applications/LibreOffice.app/Contents/MacOS/soffice')]
        for env in ['PROGRAMFILES', 'PROGRAMFILES(X86)']:
            if os.environ.get(env):
                candidates.append(Path(os.environ[env]) / 'LibreOffice/program/soffice.exe')
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)
    raise FileNotFoundError(name + ' was not found. See README.md for installation instructions.')


def build_pptx(config_path, out_dir, name):
    config = json.loads(config_path.read_text(encoding='utf-8'))
    src = ROOT / 'src/pptx'
    parts = {p.relative_to(src).as_posix(): p.read_bytes() for p in src.rglob('*') if p.is_file()}
    for required in ['[Content_Types].xml', '_rels/.rels', 'ppt/presentation.xml', 'ppt/slides/slide1.xml']:
        if required not in parts:
            raise FileNotFoundError('Missing source part: ' + required)
    parts = apply_config(parts, config)
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / (name + '.pptx')
    with ZipFile(destination, 'w', ZIP_DEFLATED) as z:
        for path, data in sorted(parts.items()):
            info = ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            z.writestr(info, data)
    return destination


def export_pdf(pptx, soffice):
    with tempfile.TemporaryDirectory(prefix='qldpc-poster-') as temp:
        folder = Path(temp).resolve()
        profile = folder / 'profile'
        result = subprocess.run([
            soffice, '-env:UserInstallation=' + profile.as_uri(), '--headless',
            '--convert-to', 'pdf', '--outdir', str(folder), str(pptx),
        ], capture_output=True, text=True, timeout=180)
        generated = folder / (pptx.stem + '.pdf')
        if result.returncode != 0 or not generated.is_file() or generated.stat().st_size == 0:
            raise RuntimeError('PDF conversion failed:\n' + result.stdout + result.stderr)
        destination = pptx.with_suffix('.pdf')
        shutil.copyfile(generated, destination)
        return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'poster.json')
    parser.add_argument('--out-dir', type=Path, default=ROOT / 'build')
    parser.add_argument('--name', default='qldpc_poster_v10')
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--soffice', help='Optional path to LibreOffice executable')
    parser.add_argument('--pdftoppm', help='Optional path to Poppler pdftoppm executable')
    parser.add_argument('--preview-size', type=int, default=1800)
    args = parser.parse_args()
    if Path(args.name).name != args.name or not re.fullmatch(r'[A-Za-z0-9_-]+', args.name):
        parser.error('--name must contain only letters, digits, underscores and hyphens')
    if args.preview_size <= 0:
        parser.error('--preview-size must be positive')
    # Resolve conversion tools before writing so a missing dependency is clear.
    soffice = find_executable(args.soffice, 'soffice') if args.pdf or args.preview else None
    pdftoppm = find_executable(args.pdftoppm, 'pdftoppm') if args.preview else None
    pptx = build_pptx(args.config.resolve(), args.out_dir.resolve(), args.name)
    print(pptx)
    if soffice:
        pdf = export_pdf(pptx, soffice)
        print(pdf)
        if pdftoppm:
            prefix = pdf.parent / (pdf.stem + '_preview')
            subprocess.run([pdftoppm, '-scale-to', str(args.preview_size), '-singlefile', '-png', str(pdf), str(prefix)], check=True, timeout=120)
            png = prefix.with_suffix('.png')
            if not png.is_file() or png.stat().st_size == 0:
                raise RuntimeError('Preview was not created')
            with png.open('rb') as stream:
                if stream.read(8) != b'\x89PNG\r\n\x1a\n':
                    raise RuntimeError('Preview is not a PNG file')
                stream.seek(-12, 2)
                if stream.read() != b'\x00\x00\x00\x00IEND\xaeB\x60\x82':
                    raise RuntimeError('Preview PNG is truncated; check the pdftoppm executable')
            print(png)


if __name__ == '__main__':
    main()
