#
# Copyright (c) 2018, 2019, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as
# published by the Free Software Foundation.
#
# This program is also distributed with certain software (including
# but not limited to OpenSSL) that is licensed under separate terms,
# as designated in a particular file or component or in included license
# documentation.  The authors of MySQL hereby grant you an
# additional permission to link the program and your derivative works
# with the separately licensed software that they have included with
# MySQL.
#
# Without limiting anything contained in the foregoing, this file,
# which is part of MySQL Connector/C++, is also subject to the
# Universal FOSS Exception, version 1.0, a copy of which can be found at
# http://oss.oracle.com/licenses/universal-foss-exception.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License, version 2.0, for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA

# Arguments that can be fiven to "rpmbuild"
#
#  mysql_dir     Path to the MySQL installation, where to find the client lib
#  commercial    If set, is a commercial build

%{?mysql_dir:    %global mysql_opt -DMYSQL_DIR=%{mysql_dir}}
%{!?commercial:  %global license_type GPLv2}
%{?commercial:   %global license_type Commercial}
%{?commercial:   %global product_suffix -commercial}
%{!?commercial:  %global product_suffix %{nil}}

%{?el6:%global __strip /opt/rh/devtoolset-7/root/usr/bin/strip}

%if 0%{?suse_version} == 1315
%global dist            .sles12
%endif

%if 0%{?suse_version} == 1500
%global dist            .sl15
%endif

Summary:        MySQL database connector for C++
Name:           mysql-connector-c++%{?product_suffix}
Version:	1.0
Release:        1%{?commercial:.1}%{?dist}
License:        %{license_type}
URL:            https://dev.mysql.com/doc/connector-cpp/en/
Source0:        https://dev.mysql.com/get/Downloads/Connector-C++/mysql-connector-c++%{?product_suffix}-%{version}.tar.gz
#BuildRequires:  boost-devel
%if 0%{?rhel}
BuildRequires:  cmake3
%else
BuildRequires:  cmake
%endif
%if 0%{?fedora} || 0%{?suse_version} || 0%{?rhel} >= 8
BuildRequires:  gcc
BuildRequires:  gcc-c++
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
%{!?mysql_dir:BuildRequires: mysql-devel}
BuildRequires:  openssl-devel
%{?commercial:Obsoletes: mysql-connector-c++ < %{version}-%{release}}
%description
A C++ interface for communicating with MySQL servers.

%package        devel
Summary:        Development header files and libraries for MySQL C++ client applications
%if 0%{?commercial}
Requires:       mysql-connector-c++-commercial =  %{version}-%{release}
Obsoletes:      mysql-connector-c++-devel < %{version}-%{release}
%else
Requires:       mysql-connector-c++ =  %{version}-%{release}
%endif
%description    devel
This package contains the development header files and libraries necessary
to develop MySQL client applications in C++.

%if 0%{?with_tests:1} && 0%{?with_gtest:1}
%package        test
Summary:        Regression tests for MySQL Connector/C++
%if 0%{?commercial}
Requires:       mysql-connector-c++-commercial =  %{version}-%{release}
Obsoletes:      mysql-connector-c++-test < %{version}-%{release}
%else
Requires:       mysql-connector-c++ =  %{version}-%{release}
%endif
%description    test
This package contains the test files necessary to run regression
test suite for MySQL Connector/C++
%endif

%prep
%setup -q -n mysql-connector-c++%{product_suffix}-%{version}

%build
%if 0%{?rhel} < 8
%{?rhel:export CC=gcc}
%{?rhel:export CXX=g++}
%endif

%if 0%{?with_tests:1} && 0%{?with_gtest:1}
%global __cmake_test_opts -DWITH_TESTS=1 -DWITH_GTEST=%{with_gtest}
%else
%global __cmake_test_opts %{nil}
%endif

%global __cmake_explicit_opts -DCMAKE_INSTALL_PREFIX="%_prefix" -DCMAKE_C_FLAGS:STRING="%optflags" -DCMAKE_CXX_FLAGS:STRING="%optflags"
%global __cmake_common_opts -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir}/mysql-cppconn-8 -DWITH_JDBC=OFF -DWITH_SSL=system %{__cmake_test_opts} %{?mysql_opt} -DDEBUG_PREFIX_MAP=OFF

%if 0%{?rhel}
%global __cmake_cmd cmake3 %{__cmake_common_opts} %{__cmake_explicit_opts} ..
%else
%global __cmake_cmd cmake %{__cmake_common_opts} %{__cmake_explicit_opts} ..
%endif

mkdir build-dynamic && pushd build-dynamic
pwd
%__cmake_cmd
make %{?_smp_mflags} VERBOSE=1
popd

mkdir build-static && pushd build-static
%__cmake_cmd -DBUILD_STATIC=ON
make %{?_smp_mflags} VERBOSE=1
popd

%install
pushd build-dynamic
make DESTDIR=%{buildroot} install

%if 0%{?with_tests:1} && 0%{?with_gtest:1}
# Generating the test groups and run CMake again
# to process the generated TestGroups.cmake file
LD_LIBRARY_PATH=. ./run_unit_tests --generate_test_groups=TestGroups.cmake
%__cmake_cmd
# Move the test executable and test definition to private libdir
install -d -m0755 %{buildroot}%{_libdir}/mysql-cppconn-8/dynamic
mv CTestTestfile.cmake %{buildroot}%{_libdir}/mysql-cppconn-8/dynamic/
mv run_unit_tests      %{buildroot}%{_libdir}/mysql-cppconn-8/dynamic/
%endif
popd

pushd build-static
make DESTDIR=%{buildroot} install

%if 0%{?with_tests:1} && 0%{?with_gtest:1}
# Generating the test groups and run CMake again
# to process the generated TestGroups.cmake file
./run_unit_tests --generate_test_groups=TestGroups.cmake
%__cmake_cmd -DBUILD_STATIC=ON
# Move the test executable and test definition to private libdir
install -d -m0755 %{buildroot}%{_libdir}/mysql-cppconn-8/static
mv CTestTestfile.cmake %{buildroot}%{_libdir}/mysql-cppconn-8/static/
mv run_unit_tests      %{buildroot}%{_libdir}/mysql-cppconn-8/static/
%endif
popd

# Add compat dir and remove unwanted file
ln -s mysql-cppconn-8 %{buildroot}%{_includedir}/mysql-cppconn
rm %{buildroot}/usr/{INFO_SRC,INFO_BIN}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.txt LICENSE.txt INFO_SRC build-dynamic/INFO_BIN
%{_libdir}/libmysqlcppconn8.so.*
%{_libdir}/libmysqlcppconn8.so.2*


%files devel
%doc README.txt LICENSE.txt INFO_SRC build-dynamic/INFO_BIN
%{_libdir}/libmysqlcppconn8.so
%{_libdir}/libmysqlcppconn8-static.a
%{_includedir}/mysql-cppconn
%dir %{_includedir}/mysql-cppconn-8
%{_includedir}/mysql-cppconn-8/mysqlx
%{_includedir}/mysql-cppconn-8/mysql

%if 0%{?with_tests:1} && 0%{?with_gtest:1}
%files test
%dir %{_libdir}/mysql-cppconn-8
%dir %{_libdir}/mysql-cppconn-8/dynamic
%dir %{_libdir}/mysql-cppconn-8/static
%{_libdir}/mysql-cppconn-8/dynamic/run_unit_tests
%{_libdir}/mysql-cppconn-8/dynamic/CTestTestfile.cmake
%{_libdir}/mysql-cppconn-8/static/run_unit_tests
%{_libdir}/mysql-cppconn-8/static/CTestTestfile.cmake
%endif

%changelog
* Fri Feb 15 2019 Bjorn Munch <bjorm.munch@oracle.com> - 8.0.16-1
- CMake 3 should not be used on Fedora, only on Oracle Linux or Red Hat
- Removed use of cmake_path as it is no longer needed

* Thu Feb 14 2019 Rafal Somla <rafal.somla@oracle.com>
- Use ABI version number taken from version.cmake in %files patterns

* Fri Dec 14 2018 Kent Boortz <kent.boortz@oracle.com> - 8.0.15-1
- Use CMake 3 on Fedora and Oracle Linux
- Added option to specify what CMake to use, "--define 'cmake_path <path>'"

* Tue Nov 27 2018 Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 8.0.14-1
- Added INFO_BIN and INFO_SRC files

* Fri Aug 24 2018 Kent Boortz <kent.boortz@oracle.com> - 8.0.13-1
- Added "test" package

* Wed May 16 2018 Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 8.0.11-1
- Adapt to MySQL Connector C++ 8.0

* Tue Apr 05 2016 Kent Boortz <kent.boortz@oracle.com> - 2.0.1-1
- initial package
