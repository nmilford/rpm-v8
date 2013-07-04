rpm-v8
======

An RPM spec file to build and install the V8 JavaScript Engine.

To build:

`sudo yum -y install rpmdevtools && rpmdev-setuptree`

`sudo yum -y install python26 gcc44-c++ subversion`

`wget https://raw.github.com/nmilford/rpm-v8/master/v8.spec -O ~/rpmbuild/SPECS/v8.spec`

`rpmbuild -bb ~/rpmbuild/SPECS/v8.spec`
