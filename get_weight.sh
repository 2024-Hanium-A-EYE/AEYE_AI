#############################################################
# AEYE AI Weight Fetcher
# Created By Yoonchul Chung
# Created At 2024.08.16
# Welcome to Visit Github : https://github.com/Yoonchulchung
#############################################################


install_mega_cloud()
{
    apt-get update
    apt-get install figlet

    figlet install
    figlet MEGA

    apt-get install wget gnupg
    wget -qO - https://mega.nz/keys/MEGA_signing.key | apt-key add -
    echo "deb https://mega.nz/linux/repo/xUbuntu_$(lsb_release -rs) ./" | tee /etc/apt/sources.list.d/mega.list
    apt-get update
    apt-get install megacmd -y
}

get_weight_file()
{
    cd AEYE_Network_Operator/mw/views/weight && mega-get 'https://mega.nz/file/LVw0UahD#WOjbPdOBZ0RiR2wN-xJ42I8seW6x5FSQTjfTvwdxI5I' 
    
}

run()
{
    install_mega_cloud
    get_weight_file
}

run