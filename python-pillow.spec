%global py2_incdir %{_includedir}/python%{python_version}
%global py3_incdir %{_includedir}/python%{python3_version}

%global name3 python%{python3_pkgversion}-pillow

# RHEL-7 does have python 3.4
%if 0%{?rhel} >= 7
  %global with_python3 1
%endif

# Refer to the comment for Source0 below on how to obtain the source tarball
# The saved file has format python-imaging-Pillow-$version-$ahead-g$shortcommit.tar.gz
%global commit d1c6db88d4dee462c6bbf4e22555e3ddd410d06a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global ahead 105

# If ahead is 0, the tarball corresponds to a release version, otherwise to a git snapshot
%if %{ahead} > 0
%global snap .git%{shortcommit}
%endif

Name:           python-pillow
Version:        2.0.0
Release:        20%{?snap}%{?dist}
Summary:        Python image processing library

# License: see http://www.pythonware.com/products/pil/license.htm
License:        MIT
URL:            http://python-pillow.github.io/

# Obtain the tarball for a certain commit via:
#  wget --content-disposition https://github.com/python-imaging/Pillow/tarball/$commit
Source0:        https://github.com/python-imaging/Pillow/tarball/%{commit}/python-imaging-Pillow-%{version}-%{ahead}-g%{shortcommit}.tar.gz

# Add s390* and ppc* archs
Patch0:         python-pillow-archs.patch
# Fix test hardcoded for little-endian
Patch1:         python-pillow_endian.patch
Patch2:         python-pillow-2.0.0_bytearray.patch
Patch3:         python-pillow-2.0.0_memleaks.patch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  tkinter
BuildRequires:  tk-devel
BuildRequires:  python-sphinx
BuildRequires:  libjpeg-devel
BuildRequires:  zlib-devel
BuildRequires:  freetype-devel
BuildRequires:  sane-backends-devel
# Don't build with webp support on s390* and ppc* archs
# see bug #962091 and #1127230
%ifnarch s390 s390x ppc ppc64
BuildRequires:  libwebp-devel
%endif
BuildRequires:  PyQt4
BuildRequires:  numpy

%if %{with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-tkinter
#BuildRequires: python%{python3_pkgversion}-PyQt4
BuildRequires:  python%{python3_pkgversion}-numpy
%endif

Provides:       python-imaging = %{version}-%{release}
Obsoletes:      python-imaging <= 1.1.7-12

%if %{with_python3}
Provides:       python%{python3_pkgversion}-imaging = %{version}-%{release}
%endif

%filter_provides_in %{python_sitearch}
%filter_provides_in %{python3_sitearch}
%filter_setup

%description
Python image processing library, fork of the Python Imaging Library (PIL)

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are five subpackages: tk (tk interface), qt (PIL image wrapper for Qt),
sane (scanning devices interface), devel (development) and doc (documentation).


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python-devel, libjpeg-devel, zlib-devel
Provides:       python-imaging-devel = %{version}-%{release}
Obsoletes:      python-imaging-devel <= 1.1.7-12

%description devel
Development files for %{name}.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%package sane
Summary:        Python module for using scanners
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       python-imaging-sane = %{version}-%{release}
Obsoletes:      python-imaging-sane <= 1.1.7-12

%description sane
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.


%package tk
Summary:        Tk interface for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       tkinter
Provides:       python-imaging-tk = %{version}-%{release}
Obsoletes:      python-imaging-tk <= 1.1.7-12

%description tk
Tk interface for %{name}.

%package qt
Summary:        PIL image wrapper for Qt
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       PyQt4
Provides:       python-imaging-qt = %{version}-%{release}

%description qt
PIL image wrapper for Qt.


%if %{with_python3}
%package -n %{name3}
Summary:        Python 3 image processing library

%description -n %{name3}
%{_description}


%package -n %{name3}-devel
Summary:        Development files for %{name3}
Group:          Development/Libraries
Requires:       %{name3}%{?_isa} = %{version}-%{release}
Requires:       python%{python3_pkgversion}-devel, libjpeg-devel, zlib-devel

%description -n %{name3}-devel
Development files for %{name3}.


%package -n %{name3}-doc
Summary:        Documentation for %{name3}
Group:          Documentation
Requires:       %{name3} = %{version}-%{release}

%description -n %{name3}-doc
Documentation for %{name3}.


%package -n %{name3}-sane
Summary:        Python module for using scanners
Group:          System Environment/Libraries
Requires:       %{name3}%{?_isa} = %{version}-%{release}

%description -n %{name3}-sane
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.


%package -n %{name3}-tk
Summary:        Tk interface for %{name3}
Group:          System Environment/Libraries
Requires:       %{name3}%{?_isa} = %{version}-%{release}
Requires:       tkinter

%description -n %{name3}-tk
Tk interface for %{name3}.

%package -n %{name3}-qt
Summary:        PIL image wrapper for Qt
Group:          System Environment/Libraries
Obsoletes:      %{name3} <= 2.0.0-5.git93a488e8
Requires:       %{name3}%{?_isa} = %{version}-%{release}
Requires:       python%{python3_pkgversion}-PyQt4

%description -n %{name3}-qt
PIL image wrapper for Qt.

%endif


%prep
%setup -q -n python-imaging-Pillow-%{shortcommit}
%patch0 -p1 -b .archs
%patch1 -p1 -b .endian
%patch2 -p1 -b .byte_array
%patch3 -p1 -b .memleaks

%if %{with_python3}
# Create Python 3 source tree
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
# Build Python 2 modules
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

pushd Sane
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
popd

pushd docs
PYTHONPATH=$PWD/.. make html
rm -f _build/html/.buildinfo
popd

%if %{with_python3}
# Build Python 3 modules
pushd %{py3dir}
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python3}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

pushd Sane
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd

pushd docs
PYTHONPATH=$PWD/.. make html
rm -f _build/html/.buildinfo
popd
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

# Install Python 2 modules
install -d $RPM_BUILD_ROOT/%{py2_incdir}/Imaging
install -m 644 libImaging/*.h $RPM_BUILD_ROOT/%{py2_incdir}/Imaging
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
pushd Sane
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd

%if %{with_python3}
# Install Python 3 modules
pushd %{py3dir}
install -d $RPM_BUILD_ROOT/%{py3_incdir}/Imaging
install -m 644 libImaging/*.h $RPM_BUILD_ROOT/%{py3_incdir}/Imaging
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
pushd Sane
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
popd
%endif

# The scripts are packaged in %%doc
rm -rf $RPM_BUILD_ROOT%{_bindir}


%check
# Check Python 2 modules
ln -s $PWD/Images $RPM_BUILD_ROOT%{python_sitearch}/Images
ln -s $PWD/Tests $RPM_BUILD_ROOT%{python_sitearch}/Tests
ln -s $PWD/selftest.py $RPM_BUILD_ROOT%{python_sitearch}/selftest.py
pushd $RPM_BUILD_ROOT%{python_sitearch}
%{__python} selftest.py
%{__python} Tests/run.py
popd
rm $RPM_BUILD_ROOT%{python_sitearch}/Images
rm $RPM_BUILD_ROOT%{python_sitearch}/Tests
rm $RPM_BUILD_ROOT%{python_sitearch}/selftest.py*

%if %{with_python3}
# Check Python 3 modules
pushd %{py3dir}
ln -s $PWD/Images $RPM_BUILD_ROOT%{python3_sitearch}/Images
ln -s $PWD/Tests $RPM_BUILD_ROOT%{python3_sitearch}/Tests
ln -s $PWD/selftest.py $RPM_BUILD_ROOT%{python3_sitearch}/selftest.py
pushd $RPM_BUILD_ROOT%{python3_sitearch}
%{__python3} selftest.py
%{__python3} Tests/run.py
popd
rm $RPM_BUILD_ROOT%{python3_sitearch}/Images
rm $RPM_BUILD_ROOT%{python3_sitearch}/Tests
rm $RPM_BUILD_ROOT%{python3_sitearch}/selftest.py*
popd
%endif


%files
%doc README.rst docs/HISTORY.txt COPYING
%{python_sitearch}/*
# These are in subpackages
%exclude %{python_sitearch}/*sane*
%exclude %{python_sitearch}/_imagingtk*
%exclude %{python_sitearch}/PIL/ImageTk*
%exclude %{python_sitearch}/PIL/SpiderImagePlugin*
%exclude %{python_sitearch}/PIL/ImageQt*

%files devel
%{py2_incdir}/Imaging/

%files doc
%doc Scripts Images docs/_build/html

%files sane
%doc Sane/CHANGES Sane/demo*.py Sane/sanedoc.txt
%{python_sitearch}/*sane*

%files tk
%{python_sitearch}/_imagingtk*
%{python_sitearch}/PIL/ImageTk*
%{python_sitearch}/PIL/SpiderImagePlugin*

%files qt
%{python_sitearch}/PIL/ImageQt*

%if %{with_python3}
%files -n %{name3}
%doc README.rst docs/HISTORY.txt COPYING
%{python3_sitearch}/*
# These are in subpackages
%exclude %{python3_sitearch}/*sane*
%exclude %{python3_sitearch}/_imagingtk*
%exclude %{python3_sitearch}/PIL/ImageTk*
%exclude %{python3_sitearch}/PIL/SpiderImagePlugin*
%exclude %{python3_sitearch}/PIL/ImageQt*

%files -n %{name3}-devel
%{py3_incdir}/Imaging/

%files -n %{name3}-doc
%doc Scripts Images docs/_build/html

%files -n %{name3}-sane
%doc Sane/CHANGES Sane/demo*.py Sane/sanedoc.txt
%{python3_sitearch}/*sane*

%files -n %{name3}-tk
%{python3_sitearch}/_imagingtk*
%{python3_sitearch}/PIL/ImageTk*
%{python3_sitearch}/PIL/SpiderImagePlugin*

%files -n %{name3}-qt
%{python3_sitearch}/PIL/ImageQt*

%endif

%changelog
