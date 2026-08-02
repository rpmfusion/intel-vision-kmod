%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

%global commit a8d772f261bc90376944956b7bfd49b325ffa2f2
%global tags WW46.3_25_ptl_pv

%global prjname vision-drivers
%global pkgname intel-vision

Name:           %{pkgname}-kmod
Summary:        Kernel module (kmod) for %{pkgname}
Version:        2025112.WW46.3_25_ptl_pv
Release:        4%{?dist}
License:        GPL-2.0-or-later

URL:            https://github.com/intel/vision-drivers
Source0:        %{url}/archive/refs/tags/%{tags}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  gcc
BuildRequires:  elfutils-libelf-devel
BuildRequires:  kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{pkgname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
This repository supports Intel Vision Driver on Intel Lunar Lake (LNL)
CVS-enabled Platforms


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{pkgname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null


%setup -q -c
for kernel_version  in %{?kernel_versions} ; do
  cp -a %{prjname}-%{tags} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done


%install
for kernel_version in %{?kernel_versions}; do
  mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/intel_cvs.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done
%{?akmod_install}


%changelog
* Sun Aug 02 2026 RPM Fusion Release Engineering <leigh123linux@rpmfusion.org> - 2025112.WW46.3_25_ptl_pv-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Tue Dec 30 2025 Kate Hsuan <hpa@redhat.com> - 2025112.WW46.3_25_ptl_pv-3
- Update ExclusiveArch

* Thu Nov 20 2025 Ben Matteson <bmatteso@us.ibm.com> - WW46.3_25_ptl_pv-2
- Update spec file

* Thu Oct 30 2025 Ben Matteson <bmatteso@us.ibm.com> - WW46.3_25_ptl_pv-1
- Update to WW46.3_25_ptl_pv
