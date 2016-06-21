
# This spec file can be used to build an RPM package for installation.
# **NOTE**
#     Version, Release, and tagname information should be updated for the
#     particular release to build an RPM for.


%define project espa-spectral-indices
%define build_timestamp %(date +"%%Y%%m%%d%%H%%M%%S")
# Specify the repository tag/branch to clone and build from
%define tagname dev_v2.5.0
# Specify the name of the directory to clone into
%define clonedname %{name}-%{tagname}
# Change the default rpm name format for the rpm built by this spec file
%define _build_name_fmt %%{NAME}.%%{VERSION}.%%{RELEASE}%{?dist}.%{ARCH}.rpm


# ----------------------------------------------------------------------------
Name:		%{project}
Version:	2.5.0
Release:	1.%{build_timestamp}
Summary:	ESPA Spectral Indices Software

Group:		ESPA
License:	NASA Open Source Agreement
URL:		https://github.com/USGS-EROS/espa-spectral-indices.git

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	x86_64
Packager:	USGS EROS LSRD

#BuildRequires:	espa-product-formatter >= 201608
Requires:	espa-product-formatter >= 201608


# ----------------------------------------------------------------------------
%description
Provides science application executables for generating spectral indice products for Landsat 4, 5, 7, and 8.  These applications are implemented in C and Python.


# ----------------------------------------------------------------------------
%prep
# We don't need to perform anything here

%build
# Start with a clean clone of the repo
rm -rf %{clonedname}
git clone --depth 1 --branch %{tagname} %{url} %{clonedname}
# Build the applications
cd %{clonedname}
make BUILD_STATIC=yes

%install
# Start with a clean installation location
rm -rf %{buildroot}
# Install the applications for a specific path
cd %{clonedname}
make install PREFIX=%{buildroot}/usr/local

%clean
# Cleanup our cloned repository
rm -rf %{clonedname}
# Cleanup our installation location
rm -rf %{buildroot}


# ----------------------------------------------------------------------------
%files
%defattr(-,root,root,-)
# All sub-directories are automatically included
/usr/local/bin/*
/usr/local/%{project}


# ----------------------------------------------------------------------------
%changelog
* Tue Jun 21 2016 Adam J Dosch <adosch@usgs.gov>
- Initial Version for August 2016 release
