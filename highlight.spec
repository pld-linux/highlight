#
# Conditional build:
%bcond_without	apidocs # don't generate apidocs subpackage
#
Summary:	A source code converter to HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Summary(pl.UTF-8):	Konwerter kodu źródłowego do formatów HTML, XHTML, RTF, TeX, LaTeX, XSL-FO oraz XML
Name:		highlight
Version:	2.4.3
Release:	1
License:	GPL
Group:		Applications/Publishing
Source0:	http://www.andre-simon.de/zip/%{name}-%{version}.tar.gz
# Source0-md5:	19b0437361f84467fff11bdbeba654a0
Patch0:		%{name}-Makefile.patch
URL:		http://www.andre-simon.de/
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _sysconfdir /etc/highlight

%description
Highlight is a universal converter from source code to HTML, XHTML,
RTF, TeX, LaTeX, XSL-FO, and XML. (X)HTML output is formatted by
Cascading Style Sheets. It supports 100 programming languages and
includes 50 highlighting color themes. It's possible to easily enhance
the parsing database. The converter includes some features to provide
a consistent layout of the input code.

%description -l pl.UTF-8
Highlight jest uniwersalnym konwerterem kodu źródłowego do formatów
HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML. Wyjście (X)HTML jest
formatowane przez kaskadowe arkusze stylów (CSS). Highlight wspiera
100 języków programowania i zawiera 50 kolorystycznych motywów
podświetlania składni. Umożliwia łatwe ulepszanie bazy parsowania.
Konwerter zawiera pewne cechy zapewniające spójny układ graficzny kodu
wejściowego.

%package apidocs
Summary:	API documentation for highlight - a source code converter to HTML, XHTML, RTF, TeX, LaTeX, XSL-FO, and XML
Summary(pl.UTF-8):	Dokumentacja API highlight - konwertera kodu źródłowego do HTML, XHTML, RTF, TeX, LaTeX, XSL-FO oraz XML
Group:		Documentation

%description apidocs
API documentation for highlight - a source code converter to HTML,
XHTML, RTF, TeX, LaTeX, XSL-FO, and XML.

%description apidocs -l pl.UTF-8
Dokumentacja API highlight - konwertera kodu źródłowego do formatu
HTML, XHTML, RTF, TeX, LaTeX, XSL-FO oraz XML.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}"

%{?with_apidocs:%{__make} apidocs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# to avoid false `warning: Installed (but unpackaged) file(s) found:' - these files are packaged through %doc
rm -fr $RPM_BUILD_ROOT/usr/share/doc/highlight

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README README_INDENT README_REGEX TODO examples
%lang(de) %doc README_DE
%lang(es) %doc README_ES
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs/html/*
%endif
