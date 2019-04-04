# Prerequest 
```
sudo apt-get update 
sudo apt-get install build-essential automake autoconf libtool
sudo apt-get install libxml++2.6-dev
sudo apt-get install swig 
sudo apt-get install subversion
```

If you don't have anaconda installed, please do that. Let's assume your anaconda locates in: 
```
~/anaconda3
``` 

# Installation
* Create a virtual Python with python2.7
```
conda create -n ghmm python=2.7 pip
```

Then you will have a directory at
```
~/anaconda3/envs/ghmm
```
Don't foget to activate your virtual python env. 
```
conda activate ghmm
```

* Download the GHMM source code. 
```
svn checkout svn://svn.code.sf.net/p/ghmm/code/trunk/ghmm ghmm
``` 

* Compile 
```
cd ghmm 
./autogen.sh
./configure --without-python --prefix=~/anaconda3/envs/ghmm/
make
make install 
cd ghmmwrapper/
python setup.py build 
python setuy.py install --prefix=~/anaconda3/envs/ghmm/
``` 


# Test it. 
Open a python
```
Pyhon
```

Then import the module. 
```
import ghmm
```


