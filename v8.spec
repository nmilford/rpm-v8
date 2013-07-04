# To build:
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# sudo yum -y install python26 gcc44-c++ subversion
# wget https://raw.github.com/nmilford/rpm-v8/master/v8.spec -O ~/rpmbuild/SPECS/v8.spec
# rpmbuild -bb ~/rpmbuild/SPECS/v8.spec

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
#%{!?python26_sitelib: %global python26_sitelib %(python26 -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           v8
Version:        3.9.24.37
Release:        1
Summary:        JavaScript Engine
Group:          System Environment/Libraries
License:        BSD
URL:            http://code.google.com/p/v8
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  subversion
BuildRequires:  python26
BuildRequires:  gcc44-c++

%description
V8 is Google's open source JavaScript engine. V8 is written in C++ and is used 
in Google Chrome, the open source browser from Google. V8 implements ECMAScript 
as specified in ECMA-262, 3rd edition.

%package devel
Group:          Development/Libraries
Summary:        Development headers and libraries for v8
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers, libraries and tools for v8.

%build
# Grab the code.
svn export http://v8.googlecode.com/svn/tags/%{version}/ v8-%{version}
cd v8-%{version}

# Grb the GYP build tool.
make dependencies

# Make GYP use python26 since CentOS5 uses python24.
find build/gyp/ -type f -print0 | xargs -0 sed -i 's/python/python26/g'

# Use g++ 4.4
export CXX=g++44 
# Build it
make native %{_smp_mflags} \
            library=shared \
            soname=on \
            protectheap=on \
            sample=shell \
            env='CCFLAGS: -fPIC'

%install

install -d -m 755 %{buildroot}/%{_bindir}
install    -m 755 %{_builddir}/v8-%{version}/out/native/d8         %{buildroot}/%{_bindir}

install -d -m 755 %{buildroot}/%{_libdir}
install    -m 644 %{_builddir}/v8-%{version}/out/native/lib.target/libv8.so   %{buildroot}/%{_libdir}/

install -d -m 755 %{buildroot}/%{_includedir}
install    -m 644 %{_builddir}/v8-%{version}/include/*.h %{buildroot}/%{_includedir}

install -d -m 755 %{buildroot}/%{python_sitelib}
install    -m 644 %{_builddir}/v8-%{version}/tools/jsmin.py %{buildroot}/%{python_sitelib}
install    -m 644 %{_builddir}/v8-%{version}/tools/js2c.py  %{buildroot}/%{python_sitelib}

# While we're at it, put it in both 2.6
#install -d -m 755 %{buildroot}/%{python26_sitelib}
#install    -m 644 %{_builddir}/v8-%{version}/tools/jsmin.py %{buildroot}/%{python26_sitelib}
#install    -m 644 %{_builddir}/v8-%{version}/tools/js2c.py  %{buildroot}/%{python26_sitelib}

install -d -m 755 %{buildroot}/usr/share/doc/v8-%{version}/
install    -m 644 %{_builddir}/v8-%{version}/AUTHORS    %{buildroot}/usr/share/doc/v8-%{version}/
install    -m 644 %{_builddir}/v8-%{version}/ChangeLog  %{buildroot}/usr/share/doc/v8-%{version}/
install    -m 644 %{_builddir}/v8-%{version}/LICENSE    %{buildroot}/usr/share/doc/v8-%{version}/
install    -m 644 %{_builddir}/v8-%{version}/LICENSE.v8 %{buildroot}/usr/share/doc/v8-%{version}/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/d8
%{_libdir}/libv8.so
/usr/share/doc/v8-%{version}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{python_sitelib}/*
#%{python26_sitelib}/*

%changelog
* Wed Jul 03 2013 Nathan Milford <nathan@milford.io> 3.9.24.37
- Initial spec... hope this is a good idea.
