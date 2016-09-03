cd /home/git
mkdir -p local
mkdir -p gogs

MACHINE_TYPE=`uname -m`
if [ ${MACHINE_TYPE} == 'armv7l' ]; then
	export VERSION_GOLANG=go1.7.linux-armv6l
elif [ ${MACHINE_TYPE} == 'x86_64' ]; then
	export VERSION_GOLANG=go1.7.linux-amd64
fi
echo "set VERSION_GOLANG to $VERSION_GOLANG"

export SOURCE_GOLANG=https://storage.googleapis.com/golang
wget $SOURCE_GOLANG/$VERSION_GOLANG.tar.gz 
echo "extract $VERSION_GOLANG.tar.gz"
tar -C /home/git/local -xzf $VERSION_GOLANG.tar.gz 

cd /home/git/
echo 'export GOROOT=$HOME/local/go' >> $HOME/.bashrc
echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> $HOME/.bashrc
echo 'source $HOME/.bashrc'
source $HOME/.bashrc

echo 'go get -u github.com/gogits/gogs'
go get -u github.com/gogits/gogs
cd $GOPATH/src/github.com/gogits/gogs
echo 'go build'
go build