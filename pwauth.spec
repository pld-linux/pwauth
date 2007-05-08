# TODO
# - we don't have group called apache
# - consider removing version from patches next time when adding to our cvs
Summary:	A Unix Web Authenticator
Name:		pwauth
Version:	2.3.2
Release:	1
License:	BSD
Group:		Daemons
URL:		http://www.unixpapa.com/pwauth/
Source0:	http://www.unixpapa.com/software/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
Patch1:		%{name}-2.3.2-config.diff
Patch2:		%{name}-2.3.2-pam.diff
Patch3:		%{name}-2.3.2-server.diff
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pwauth is an authenticator designed to be used with mod_auth_external
and the Apache HTTP Daemon to support reasonably secure web
authentication out of the system password database on most versions of
Unix.

What pwauth actually does is very simple. Given a login and a
password, it returns a status code indicating whether it is a valid
login/password or not. It is normally installed as an suid-root
program, so other programs (like Apache or a CGI program) can run it
to check if a login/password is valid even though they don't
themselves have read access to the system password database.

%prep
%setup -q
%patch1 -p0
%patch2 -p0
%patch3 -p1

#bzcat %{SOURCE1} > pwauth.pam

%build
%{__make} \
	CFLAGS="%{optflags}" \
	LIB="-lpam -ldl"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/pam.d,%{_bindir}}

install pwauth $RPM_BUILD_ROOT%{_bindir}
install unixgroup $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/pwauth
install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/unixgroup

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES FORM_AUTH INSTALL README
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/pwauth
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/unixgroup
%attr(4550,root,apache) %{_bindir}/pwauth
%attr(4550,root,apache) %{_bindir}/unixgroup
