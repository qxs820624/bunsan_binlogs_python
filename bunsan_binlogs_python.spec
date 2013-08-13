%define _builddir   .
%define _sourcedir  .
%define _specdir    .
%define _rpmdir     .

Name:       bunsan_binlogs_python
Version:    %{yandex_mail_version}
Release:    %{yandex_mail_release}
Url:        %{yandex_mail_url}

Summary:    bunsan python libraries
License:    GPLv3
Group:      System Environment/Libraries
Packager:   Aleksey Filippov <sarum9in@yandex-team.ru>
Distribution:   Red Hat Enterprise Linux

Requires:       python26
Requires:       bunsan_common_python = %{version}-%{release}
Requires:       bunsan_binlogs = %{version}-%{release}
Requires:       protobuf-python >= 2.5.0
BuildRequires:  bunsan_cmake = %{version}-%{release}
BuildRequires:  bunsan_binlogs-devel = %{version}-%{release}

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Root package for bunsan python libraries.


%package        devel
Summary:        bunsan_binlogs_python development files
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
Development files.


%build
cmake . -DCMAKE_INSTALL_PREFIX=/usr \
        -DENABLE_TESTS=NO \
        -DCMAKE_BUILD_TYPE=Release
%{__make} %{?_smp_mflags}


%install
rm -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"


%clean
%{__rm} -rf %{buildroot}


%files
%defattr (-,root,root,-)
%{_prefix}/lib/python2.6/site-packages/bunsan/binlogs/_binlogs.so
%{_prefix}/lib/python2.6/site-packages/bunsan/binlogs/__init__.py
%{_prefix}/lib/python2.6/site-packages/bunsan/binlogs/__init__.pyc
%{_prefix}/lib/python2.6/site-packages/bunsan/binlogs/__init__.pyo


%files devel
%defattr (-,root,root,-)
%{_includedir}/bunsan/binlogs/python/*


%changelog
