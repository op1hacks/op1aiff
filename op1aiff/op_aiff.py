import json
import aifc
import struct


def monkeypatch_aifc():
    # aifc doesn't support the sowt format (Signed integer (little-endian) linear PCM)
    # this works around that limitation
    _original_read_comm_chunk = aifc.Aifc_read._read_comm_chunk

    if aifc.Aifc_read._read_comm_chunk != _original_read_comm_chunk:
        return

    def _patched_read_comm_chunk(self, chunk):
        try:
            _original_read_comm_chunk(self, chunk)
        except aifc.Error:
            pass
        self._comptype = 'NONE'

    aifc.Aifc_read._read_comm_chunk = _patched_read_comm_chunk


def analyze_preset(path):
    monkeypatch_aifc()

    aif = aifc.open(path)
    print("aifc.getnchannels()", aif.getnchannels())
    print("aifc.getsampwidth()", aif.getsampwidth())
    print("aifc.getframerate()", aif.getframerate())
    print("aifc.getnframes()", aif.getnframes())
    print("aifc.getcomptype()", aif.getcomptype())
    print("aifc.getcompname()", aif.getcompname())
    print("aifc.getparams()", aif.getparams())
    print("aifc.getmarkers()", aif.getmarkers())


def read_preset(path):
    f = open(path, 'rb')
    data = f.read()
    f.close()

    # Locate start of APPL chunk
    appl_pos = data.find(bytes('APPL', 'utf-8'))
    if appl_pos == -1:
        raise TypeError('Invalid file. No APPL data found.')
    appl_pos += 4

    appl_chunk = data[appl_pos:]
    appl_data_len = struct.unpack('>l', appl_chunk[:4])[0]

    appl_data_bin = appl_chunk[4:appl_data_len+4]
    appl_data = str(appl_data_bin, 'utf-8').strip()

    if appl_data.startswith('op-1'):
        appl_data = appl_data[4:]
    return json.loads(appl_data)


def write_preset(in_file, out_file, preset_data):
    f = open(in_file, 'rb')
    data = f.read()
    f.close()

    old_appl_pos = data.find(bytes('APPL', 'utf-8'))+4

    old_appl_chunk = data[old_appl_pos:]
    old_appl_data_len = struct.unpack('>l', old_appl_chunk[:4])[0]

    start_data = data[:old_appl_pos]

    # Add 4 to account for 'APPL'
    end_data = data[old_appl_pos+old_appl_data_len+4:]

    json_data = json.dumps(preset_data, separators=(',', ':'))

    new_appl_data = bytes('op-1' + json_data + '\n ', 'utf-8')
    new_appl_chunk = struct.pack('>l', len(new_appl_data)) + new_appl_data

    new_data = start_data + new_appl_chunk + end_data

    f = open(out_file, 'wb')
    f.write(new_data)
    f.close()
