#
# spec file for package squashfuse
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define so_version 0
Name:           squashfuse
Version:        0.5.0
Release:        150500.1.3
Summary:        FUSE module to mount squashfs images
License:        BSD-2-Clause
Group:          System/Filesystems
URL:            https://github.com/vasi/squashfuse
Source:         https://github.com/vasi/squashfuse/releases/download/v%{version}/squashfuse-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  fdupes
BuildRequires:  pkgconfig(fuse)
BuildRequires:  gcc
BuildRequires:  libattr-devel
#BuildRequires:  liblzma5
BuildRequires:  libtool
BuildRequires:  pkgconfig(fuse)
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  sed
BuildRequires:  xz-devel
BuildRequires:  pkgconfig(zlib)
Requires:       fuse

%description
Squashfuse is a FUSE filesystem that allows a
squashfs archive to be mounted in user-space.
It is designed to be fast and memory-efficient,
and supports most of the features of the squashfs format.

%package -n libsquashfuse%{so_version}
Summary:        FUSE module to mount squashfs images

%description -n libsquashfuse%{so_version}
Squashfuse is a FUSE filesystem that allows a
squashfs archive to be mounted in user-space.
It is designed to be fast and memory-efficient,
and supports most of the features of the squashfs format.

%package tools
Summary:        Squafs Tools for squashfsfuse

%description tools
Demo tools from squashfsfuse package to list and extract files from a
squashfs file system (no man pages).

%package devel
Summary:        FUSE module to mount squashfs images
Group:          Development/Languages/C and C++
Requires:       libsquashfuse%{so_version} = %{version}

%description devel
Squashfuse is a FUSE filesystem that allows a
squashfs archive to be mounted in user-space.
It is designed to be fast and memory-efficient,
and supports most of the features of the squashfs format.

This package contains development files.

%prep
%setup -q

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
mkdir -p %{buildroot}%{_includedir}/squashfuse
cp *.h -v %{buildroot}%{_includedir}/squashfuse
sed -e 's,^#include ",#include "squashfuse/,' \
    %{buildroot}%{_includedir}/squashfuse/squashfuse.h \
  > %{buildroot}%{_includedir}/squashfuse.h
sed -i 's,^Libs: \(.*\),Libs: \1 -llzo2,' \
    %{buildroot}%{_libdir}/pkgconfig/squashfuse.pc
find %{buildroot} -type f \( -name "*.a" -o -name "*.la" \) -delete -print
pwd
install -m 0755 .libs/squashfuse_ls .libs/squashfuse_extract %{buildroot}/%{_bindir}

%fdupes %{buildroot}%{_includedir}
%fdupes %{buildroot}%{_libdir}

%post -n libsquashfuse%{so_version} -p /sbin/ldconfig
%postun -n libsquashfuse%{so_version} -p /sbin/ldconfig

%files
%{_mandir}/*/*
%license LICENSE
%{_bindir}/squashfuse
%{_bindir}/squashfuse_ll

%files tools
%{_bindir}/squashfuse_ls
%{_bindir}/squashfuse_extract

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/squashfuse
%{_includedir}/squashfuse.h

%files -n libsquashfuse%{so_version}
%{_libdir}/libsquashfuse.so.%{so_version}
%{_libdir}/libsquashfuse.so.%{so_version}.*
%{_libdir}/libsquashfuse_ll.so.%{so_version}
%{_libdir}/libsquashfuse_ll.so.%{so_version}.*

%changelog
* Wed Oct 18 2023 eich@suse.com
- update to version 0.5.0
  * Add --notify_fd option
  * Add --subdir option for mounting a subdirectory
  * Enable multithreading in squashfuse_ll by default
  * Fix bug that swapped the "trusted" and "security" extended
    attribute prefixes, often resulting in "No data available"
    errors.
  * Add multithreading support to squashfuse_ll, disabled by
    default but can be enabled with configure
  - -enable-multithreading Improve SIGTERM handling to do lazy
    unmount
  * Add "-o uid" and "-o gid" options to squashfuse_ll, similar
    to the corresponding FUSE library for high-level options
  * Add support for LZMA legacy images Add squashfuse_ll man
    page and reconcile help messages with man pages
  * Fix code to work with c99
  * Use optimized linux byteswap macros if available.
  * Fix "No such file or directory" when launched with empty
    fd 0.
  * Negative cache failed lookups. This saves a FUSE operation
    when repeatedly looking up non-existent files.
  * Split squashfuse_ll into a lib and executable
  * Remove redundant #if in ll header
  * Various bug fixes, new platform support
- Remove appimage patch squashfuse_from_appimage.patch
  and rpmlint file.
- Ship internal demo tools in a separate `-tools` package.
* Sun Dec  5 2021 jayvdb@gmail.com
- Replace _service with upstream tarball
- Add squashfuse.rpmlintrc
- Tidy spec and run fdupes
* Thu Jun 24 2021 tuukka.pasanen@ilmi.fi
- update to version 0.1.104
- Various bug fixes
- new platform support
- Support libfuse version 3.
- MacOS idle timeout support
* Thu Oct 17 2019 adrian@suse.de
- update to version 0.1.103
- split package to prepare for factory inclusion
* Sun Oct 12 2014 Yarny@public-files.de
- squashfuse 0.1
