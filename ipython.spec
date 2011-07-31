%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global run_testsuite 1

Name:           ipython
Version:        0.11
Release:        1%{?dist}
Summary:        An enhanced interactive Python shell

Group:          Development/Libraries
# See bug #603178 for a quick overview for the choice of licenses
# most files are under BSD and just a few under Python or MIT
# There are some extensions released under GPLv2+
License:        (BSD and MIT and Python) and GPLv2+
URL:            http://ipython.org/
Source0:        http://archive.ipython.org/release/%{version}/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-simplegeneric

%if %{run_testsuite}
# for checking/testing
BuildRequires:  python-zmq
BuildRequires:  python-zmq-tests
BuildRequires:  pexpect
BuildRequires:  python-mglob
BuildRequires:  python-simplegeneric
BuildRequires:  pyparsing
%endif

Requires:       python-zmq

#bundled libs
Requires:       pexpect
Requires:       python-mglob
Requires:       python-simplegeneric
Requires:       pyparsing

%if ! (0%{?fedora} > 13)
# argparse is in python 2.7 and 3.2
Requires:       python-argparse
%endif


%description

IPython provides a replacement for the interactive Python interpreter with
extra functionality.

Main features:
 * Comprehensive object introspection.
 * Input history, persistent across sessions.
 * Caching of output results during a session with automatically generated
   references.
 * Readline based name completion.
 * Extensible system of 'magic' commands for controlling the environment and
   performing many tasks related either to IPython or the operating system.
 * Configuration system with easy switching between different setups (simpler
   than changing $PYTHONSTARTUP environment variables every time).
 * Session logging and reloading.
 * Extensible syntax processing for special purpose situations.
 * Access to the system shell with user-extensible alias system.
 * Easily embeddable in other Python programs.
 * Integrated access to the pdb debugger and the Python profiler.

%package tests
Summary:        Tests for %{name}
Group:          Documentation
Requires:       python-nose
Requires:       python-zmq-tests
Requires:       %{name} = %{version}-%{release}
%description tests
This package contains the tests of %{name}.
You can check this way, you can test, if ipython works on your platform.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation
%description doc
This package contains the documentation of %{name}.


%package gui
Summary:        Gui applications from %{name}
Group:          Applications/Editors
Requires:       %{name} = %{version}-%{release}
Requires:       PyQt
%description gui
This package contains the gui of %{name}, which requires PyQt.



%prep
%setup -q

# delete bundling libs
pushd IPython/external
# python's own modules
rm argparse/_argparse.py

# other packages exist in fedora
rm mglob/_mglob.py
rm simplegeneric/_simplegeneric.py
rm pyparsing/_pyparsing.py
rm pexpect/_pexpect.py

# probably from here http://code.activestate.com/recipes/163604-guid/
# python has a own uuid module
#rm guid/_guid.py

# rejected in a PEP, probably no upstream
#rm Itpl/_Itpl.py

# available at pypi
#rm path/_path.py

# ssh modules from paramiko

popd


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# ipython installs docs automatically, but in the wrong place
mv %{buildroot}%{_datadir}/doc/%{name} \
    %{buildroot}%{_datadir}/doc/%{name}-%{version}


%clean
rm -rf %{buildroot}


%if %{run_testsuite}
%check
PYTHONPATH=%{buildroot}%{python_sitelib} %{buildroot}%{_bindir}/iptest || echo "some tests failed, continue..."
%endif


%files
# -f notests.files
%defattr(-,root,root,-)
%{_bindir}/ipython
%{_bindir}/irunner
%{_bindir}/pycolor
%{_bindir}/ipcluster
%{_bindir}/ipcontroller
%{_bindir}/ipengine
%{_bindir}/iplogger
%{_mandir}/man*/ipython.*
%{_mandir}/man*/ipengine*
%{_mandir}/man*/irunner*
%{_mandir}/man*/pycolor*
%{_mandir}/man*/ipc*
%{_mandir}/man*/iplogger*

%dir %{python_sitelib}/IPython
%{python_sitelib}/IPython/external
%{python_sitelib}/IPython/*.py*
%dir %{python_sitelib}/IPython/kernel
%{python_sitelib}/IPython/kernel/*.py*
%dir %{python_sitelib}/IPython/testing
%{python_sitelib}/IPython/testing/*.py*
%{python_sitelib}/IPython/testing/plugin
%{python_sitelib}/ipython-%{version}-py?.?.egg-info

%{python_sitelib}/IPython/config/
%{python_sitelib}/IPython/core/
%{python_sitelib}/IPython/extensions/
%dir %{python_sitelib}/IPython/frontend/
%{python_sitelib}/IPython/frontend/terminal/
%{python_sitelib}/IPython/frontend/__init__.py*
%{python_sitelib}/IPython/lib/
%{python_sitelib}/IPython/parallel/
%{python_sitelib}/IPython/quarantine/
%{python_sitelib}/IPython/scripts/
%{python_sitelib}/IPython/utils/
%{python_sitelib}/IPython/zmq/
%exclude %{python_sitelib}/IPython/zmq/gui/

# tests go into subpackage
%exclude %{python_sitelib}/IPython/*/tests/
%exclude %{python_sitelib}/IPython/*/*/tests

%{python_sitelib}/IPython/.git_commit_info.ini


%files tests
%defattr(-,root,root,-)
%{_bindir}/iptest
%{python_sitelib}/IPython/*/tests
%{python_sitelib}/IPython/*/*/tests


%files doc
%defattr(-,root,root,-)
# ipython installs its own documentation, but we need to own the directory
%{_datadir}/doc/%{name}-%{version}


%files gui
%defattr(-,root,root,-)
%{python_sitelib}/IPython/zmq/gui
%{python_sitelib}/IPython/frontend/qt/


%changelog
* Mon Jul  4 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.11-1
- update to 0.11
- patches included upstream
- ipython changed bundled pretty, so redistributes it in lib now
- run testsuite
- new upstream url

* Sat Apr  9 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.10.2-1
- update to new version
- patch3 is included upstream
- fixes #663823, #649281

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10.1-3
- add fix for #646079 and use upstream fix for #628742

* Mon Oct 18 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10.1-2
- argparse is in python 2.7 and 3.2

* Wed Oct 13 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10.1-1
- unbundle a bit differently
- update to new version

* Tue Aug 31 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-8
- pycolor: wrong filename -> no crash (#628742)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 19 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-6
- add missing dependencies: pexpect and python-argparse

* Tue Jun 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-5
- two more unbundled libraries in fedora

* Mon Jun 21 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.10-4
- Update patch for import in argparse

* Fri Jun 11 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-3
- fix license tag (#603178)
- add requires on wxpython to gui subpackage (#515570)
- start unbundling the libraries - more to come (#603937)

* Tue Apr 13 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.10-2
- move docs into a subpackage
- subpackage wxPython
- subpackage tests
- use proper %%{python_site*} definitions
- make %%{files} more explicit
- add some missing R (fixes #529185, #515570)

* Tue Sep 22 2009 James Bowes <jbowes@redhat.com> - 0.10-1
- Update to 0.10

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.1-2
- Rebuild for Python 2.6

* Tue Dec 02 2008 James Bowes <jbowes@redhat.com> - 0.9.1-1
- Update to 0.9.1, specfile changes courtesy Greg Swift

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.4-2
- Rebuild for Python 2.6

* Wed Jun 11 2008 James Bowes <jbowes@redhat.com> - 0.8.4-1
- Update to 0.8.4

* Fri May 30 2008 James Bowes <jbowes@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Wed Dec 12 2007 James Bowes <jbowes@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Sun Aug 05 2007 James Bowes <jbowes@redhat.com> - 0.8.1-2
- Remove explicit requires on python-abi.

* Sun Aug 05 2007 James Bowes <jbowes@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.7.2-4
- Rebuild for new Python

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> - 0.7.2-3
- Rebuild for FC6

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> - 0.7.2-2
- Include, don't ghost .pyo files per new guidelines

* Mon Jun 12 2006 Shahms E. King <shahms@shahms.com> - 0.7.2-1
- Update to new upstream version

* Mon Feb 13 2006 Shahms E. King <shahms@shahms.com> - 0.7.1.fix1-2
- Rebuild for FC-5

* Mon Jan 30 2006 Shahms E. King <shahms@shahms.com> - 0.7.1.fix1-1
- New upstream 0.7.1.fix1 which fixes KeyboardInterrupt handling

* Tue Jan 24 2006 Shahms E. King <shahms@shahms.com> - 0.7.1-1
- Update to new upstream 0.7.1

* Thu Jan 12 2006 Shahms E. King <shahms@shahms.com> - 0.7-1
- Update to new upstream 0.7.0

* Mon Jun 13 2005 Shahms E. King <shahms@shahms.com> - 0.6.15-1
- Add dist tag
- Update to new upstream (0.6.15)

* Wed Apr 20 2005 Shahms E. King <shahms@shahms.com> - 0.6.13-2
- Fix devel release number

* Mon Apr 18 2005 Shahms E. King <shahms@shahms.com> - 0.6.13-1
- Update to new upstream version

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.12-2
- Include IPython Extensions and UserConfig directories.

* Fri Mar 25 2005 Shahms E. King <shahms@shahms.com> - 0.6.12-1
- Update to 0.6.12
- Removed unused python_sitearch define

* Tue Mar 01 2005 Shahms E. King <shahms@shahms.com> - 0.6.11-2
- Fix up %%doc file specifications
- Use offical .tar.gz, not upstream .src.rpm .tar.gz

* Tue Mar 01 2005 Shahms E. King <shahms@shahms.com> - 0.6.11-1
- Initial release to meet Fedora packaging guidelines
