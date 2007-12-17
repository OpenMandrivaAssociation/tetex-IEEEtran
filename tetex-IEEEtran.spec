%{!?_texmf: %global _texmf %(eval "echo `kpsewhich -expand-var '$TEXMFMAIN'`")}

%define texpkg      IEEEtran
%define texpkgdir   %{_texmf}/tex/latex/%{texpkg}
%define texpkgdoc   %{_texmf}/doc/latex/%{texpkg}
%define bibpkgdir   %{_texmf}/bibtex/bib/%{texpkg}
%define bstpkgdir   %{_texmf}/bibtex/bst/%{texpkg}
%define bibpkgdoc   %{_texmf}/doc/bibtex/%{texpkg}

Name:           tetex-%{texpkg}
Version:        1.7a
Release:        %mkrel 1
Epoch:          0
Summary:        Official LaTeX class for IEEE transactions journals and conferences
Group:          Publishing
License:        Artistic
URL:            http://www.ctan.org/tex-archive/help/Catalogue/entries/ieeetran.html
Source0:        ftp://ftp.dante.de/tex-archive/macros/latex/contrib/IEEEtran.zip
Requires:       tetex-latex
Requires(post): tetex
Requires(postun): tetex
BuildRequires:  tetex-latex
BuildArch:      noarch

%description
The IEEEtran class is the official LaTeX class for authors of the
Institute of Electrical and Electronics Engineers (IEEE) transactions
journals and conferences. 

%prep
%setup -q -n %{texpkg}
%{__mv} extras/tux.eps .
%{__mv} bibtex/README README_BIBTEX
%{__mv} tools/README README_TOOLS

%build

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}{%{texpkgdir},%{texpkgdoc}}
%{__cp} -a IEEEtran.cls %{buildroot}%{texpkgdir}/
%{__cp} -a tools/IEEEtrantools.sty %{buildroot}%{texpkgdir}/
%{__cp} -a IEEEtran_HOWTO.pdf %{buildroot}%{texpkgdoc}/
%{__cp} -a tools/IEEEtrantools_doc.txt %{buildroot}%{texpkgdoc}/

%{__mkdir_p} %{buildroot}{%{bibpkgdir},%{bstpkgdir},%{bibpkgdoc}}
%{__cp} -a bibtex/*.bib %{buildroot}%{bibpkgdir}/
%{__cp} -a bibtex/*.bst %{buildroot}%{bstpkgdir}/
%{__cp} -a bibtex/IEEEtran_bst_HOWTO.pdf %{buildroot}%{bibpkgdoc}/

%clean
%{__rm} -rf %{buildroot}


%post
%{_bindir}/texhash >/dev/null 2>&1 || :

%postun
%{_bindir}/texhash >/dev/null 2>&1 || :

%triggerin -- lyx
if [ $2 -gt 1 ]; then
cd %{_datadir}/lyx && \
  ./configure.py --without-latex-config > /dev/null 2>&1 ||:
fi

%triggerun -- lyx
if [ $2 -eq 0 ]; then
cd %{_datadir}/lyx && \
  ./configure.py --without-latex-config > /dev/null 2>&1 ||:
fi

%files
%defattr(0644,root,root,0755)
%doc README README_BIBTEX README_TOOLS bare_conf.tex bare_jrnl.tex tux.eps
%{texpkgdir}
%{texpkgdoc}
%{bibpkgdir}
%{bstpkgdir}
%{bibpkgdoc}
