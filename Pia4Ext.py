import os,sys,struct

def main(file):
    if not os.path.exists(file):
        print("File not exist")
        return
    data = open(file, 'rb')
    os.system("mkdir " + getFileNameWithoutExtension(file))
    fileconf = cstr(b'' + data.read(4))
    if not fileconf == "SCXA":
        print("File not readable")
        return
    datastart = struct.unpack("<I",data.read(4))[0]
    filetotal = struct.unpack("<I",data.read(4))[0]
    tnstart = (filetotal+3)*4
    print("Totaly " + str(filetotal) + " files")
    
    for i in range (filetotal):
        #findfilename
        data.seek(12+i*4,0)
        namestart,nameend = struct.unpack("<2I",data.read(8))
        if data.tell() > tnstart:
            nameend = datastart - tnstart
        namelength = nameend - namestart - 8
        #finddata
        data.seek(tnstart + namestart,0)
        fstart,flength = struct.unpack("<2I",data.read(8))
        filename = cstr(b'' + data.read(namelength))
        #readfile
        if not os.path.exists(getFilePath(getFileNameWithoutExtension(file) + "/" + filename)):
            os.makedirs(getFilePath(getFileNameWithoutExtension(file) + "/" + filename))
        wrfile = open(getFileNameWithoutExtension(file) + "/" + filename, 'wb')
        data.seek(datastart + fstart,0)
        wrfile.write(data.read(flength))
        wrfile.close()
        print("complete subfile " + str(i+1))
    data.close()
    print("Complete!")

def cstr(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    return str(s.replace(b"\x00",b"").replace(b"\x5C",b"\x2F"),encoding = "sjis",errors = "ignore")
    
def getFileNameWithoutExtension(path):
    return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]
    
def getFilePath(filename):
    return filename.rsplit('/',1)[0]
    
if __name__ =="__main__":
    if len(sys.argv) < 2 :
        exit()
    files=[]
    files=sys.argv[1:]
    for file in files:
        main(file)
    
