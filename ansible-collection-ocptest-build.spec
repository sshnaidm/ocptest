%global collection_namespace sshnaidm
%global collection_name ocptest

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        1.5.1
Release:        999%{?dist}
Summary:        Ansible collection for ocptest

License:        GPLv3+
URL:            %{ansible_collection_url}
Source:         https://github.com/sshnaidm/ocptest/archive/%{version}.tar.gz

BuildRequires:  ansible >= 2.9.10

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n ansible-ocptest-collections-%{version}
sed -i -e 's/version:.*/version: %{version}/' galaxy.yml
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
rm -fvr changelogs/ ci/ contrib/ tests/ ./galaxy.yml.in .github/ .gitignore

%build
%ansible_collection_build

%install
%ansible_collection_install

%files
%license COPYING
%doc README.md
%{ansible_collection_files}

%changelog

* Tue Feb 09 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 0.0.1-1
- Initial package
