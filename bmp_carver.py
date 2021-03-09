import os
import re
import hashlib

def main():
    infile = input()
    check_infile(infile)
    output_folder = create_output_folder(infile)
    data = read_file(infile)

    suspicious_bytes = write_all_bitmaps(data, output_folder)
    write_suspicious_bytes(data, suspicious_bytes, output_folder)

def check_infile(infile):
    if not re.search("\.bmp$", infile):
        print("File \"{}\" is not a .bmp file extension.".format(infile))

    if not os.path.exists(infile):
        print("File \"{}\" does not exist.".format(infile))
        exit()

def create_output_folder(infile):
    output_folder = infile + "_Output/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def read_file(infile):
    f = open(infile, "rb")
    data = f.read()
    f.close()
    return data

def write_bytes(filepath, bytes_arr, offset, num_bytes):
    md5sum = hashlib.md5(bytes_arr[offset:(offset + num_bytes)]).hexdigest()
    f = open(filepath, "wb")
    f.write(bytes_arr[offset:(offset + num_bytes)])
    f.close()
    print("Offset: {}, FileSize: {} bytes, MD5: {}, Path: {}".format(offset, num_bytes, md5sum, filepath))

def write_all_bitmaps(data, output_folder):
    suspicious_bytes = []
    last_byte = 0

    #find "BM" header signature
    for match in re.finditer(b"\x42\x4D", data):
        filename = str(match.start()) + ".bmp"
        filepath = output_folder + filename
        #file size is 4 bytes offset at 0x2h, little endian unsigned
        filesize = int.from_bytes(data[(match.start() + 2):(match.start() + 6)], "little", signed=False)
        write_bytes(filepath, data, match.start(), filesize)

        if last_byte < match.start():
            suspicious_bytes.append((last_byte, match.start() - last_byte))
            last_byte = match.start() + filesize
        elif last_byte == match.start():
            last_byte = match.start() + filesize

    if last_byte < len(data):
        suspicious_bytes.append((last_byte, len(data) - last_byte))
        
    return suspicious_bytes



def write_suspicious_bytes(data, suspicious_bytes, output_folder):
    for (offset, length) in suspicious_bytes:
        filename = str(offset) + ".unknown"
        filepath = output_folder + filename
        write_bytes(filepath, data, offset, length)

if __name__ == "__main__":
    main()
    

