#
# spec file for package parallax
#

%define project        github.com/sarus-suite/parallax

Name:           parallax
Version:        0.6.3
Release:        150600.0.0.0
Summary:        Parallax is a lightweight Go utility that optimizes Podman for HPC systems.
License:        BSD-3-Clause
Group:          System/Management
URL:            https://%{project}
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  device-mapper-devel
BuildRequires:  libbtrfs-devel
# at least go 1.22 is needed from go.mod
BuildRequires:  golang(API) >= 1.22
Requires:  fuse-overlayfs
Requires:  squashfs
Requires:  squashfuse
Requires:  inotify-tools
Requires:  rsync

%description
Parallax is a lightweight Go utility that optimizes Podman for HPC systems by enabling fast, read-only container image storage using SquashFS on parallel filesystems (e.g., NFS). It allows seamless migration of images to shared locations, avoiding redundant pulls across cluster nodes while maintaining compatibility with existing workflows.

%prep
%autosetup -p1

%build
# Build parallax
go mod tidy
go build -o parallax

%check
# Too many tests fail due to the restricted permissions in the build enviroment.
# Updates must be tested manually.

%install
mkdir -p %{buildroot}%{_prefix}/bin
mkdir -p %{buildroot}%{_prefix}/libexec/parallax
install -m 0755 -t %{buildroot}%{_prefix}/bin parallax
install -m 0755 -t %{buildroot}%{_prefix}/libexec/parallax scripts/parallax-mount-program.sh

%files
# Binaries
%{_bindir}/parallax
# _libexec on Suse expands to /usr/lib
%{_prefix}/libexec/parallax/parallax-mount-program.sh


%changelog
* Tue Jul  8 2025 thomas.green@bristol.ac.uk
- Initial release
  * Test release.
