cd /home/git
mkdir -p local

MACHINE_TYPE=`uname -m`
if [ ${MACHINE_TYPE} == 'armv7l' ]; then
	export VERSION_GOLANG=go1.7.linux-armv6l
elif [ ${MACHINE_TYPE} == 'x86_64' ]; then
	export VERSION_GOLANG=go1.7.linux-amd64
fi
echo "set VERSION_GOLANG to $VERSION_GOLANG"

export SOURCE_GOLANG=https://storage.googleapis.com/golang
wget $SOURCE_GOLANG/$VERSION_GOLANG.tar.gz
tar -C /home/git/local -xzf go*.tar.gz

cd ~
echo 'export GOROOT=$HOME/local/go' >> $HOME/.bashrc
echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> $HOME/.bashrc
source $HOME/.bashrc

go get -u github.com/gogits/gogs
cd $GOPATH/src/github.com/gogits/gogs
go build