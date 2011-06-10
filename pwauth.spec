# TODO
# - consider removing version from patches next time when adding to our cvs
Summary:	A Unix Web Authenticator
Summary(pl.UTF-8):	Narzędzie uwierzytelniające dla WWW
Name:		pwauth
Version:	2.3.9
Release:	1
License:	BSD
Group:		Daemons
Source0:	http://pwauth.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	eaa28b0a1faea428b0af574f8fe87d55
Source1:	%{name}.pam
Patch0:		%{name}-config.patch
Patch1:		%{name}-strchr.patch
URL:		http://www.unixpapa.com/pwauth/
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

%description -l pl.UTF-8
pwauth to narzędzie uwierzytelniające zaprojektowane do używania wraz
z mod_auth_external i demonem HTTP Apache w celu obsługi w miarę
bezpiecznego uwierzytelniania przez WWW względem systemowej bazy
danych haseł na większości wersji Uniksa.

To, co robi pwauth, jest bardzo proste. Po podaniu loginu i hasła
zwraca kod wyjścia oznaczający, czy login i hasło były prawidłowe czy
nie. Zwykle instaluje się go jako program suid root, aby inne programy
(takie jak Apache czy programy CGI) mogły uruchomić go w celu
sprawdzenia poprawności loginu/hasła nawet jeśli same nie mogą
przeczytać systemowej bazy danych haseł.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
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
%attr(4754,root,http) %{_bindir}/pwauth
%attr(4754,root,http) %{_bindir}/unixgroup
