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
echo 'export GOROOT=/home/git/local/go' >> /home/git/.bashrc
echo 'export GOPATH=/home/git/go' >> /home/git/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> /home/git/.bashrc
echo 'source /home/git/.bashrc'
source /home/git/.bashrc

whoami
echo 'go get -u github.com/gogits/gogs'
/home/git/go/bin/go get -u github.com/gogits/gogs
cd $GOPATH/src/github.com/gogits/gogs
echo 'go build'
/home/git/go/bin/go build