import os
import subprocess
output = subprocess.getoutput("lsof /dev/snd/*")
print(output.split(" "))
my_list = output.split(" ")
if '/dev/snd/pcmC1D0c\nffmpeg' in my_list:
    print("exists")
    my_index = my_list.index("/dev/snd/pcmC1D0c\nffmpeg")
    print(my_index + 4)
    my_required_index = my_index + 4
    print(my_list[my_required_index])
    my_command = "sudo kill -9 " + str((my_list[my_required_index]))
    print(my_command)
    os.system(my_command)
# os.system("nmcli radio wifi off")