tests:
	tools/run-tests.sh

deb: clean
	tools/update-deb.sh

update-submodules:
	tools/update-submodules.sh

obs: deb
	tools/update-obs-packages.sh

new-plugin:
	tools/new-plugin.py

clean:
	rm -f *.debian.tar.gz
	rm -f *.orig.tar.gz
	rm -f *.dsc
	rm -f *.changes
	rm -f *.deb

	rm -f plugins/*.orig.tar.gz
	rm -f plugins/*.debian.tar.gz
	rm -f plugins/*.dsc
	rm -f plugins/*.changes
	rm -f plugins/*.deb

	rm -f plugins/*/debian/plugin-*/ -r
	rm -f plugins/*/debian/files
	rm -f plugins/*/debian/*.debhelper.log
	rm -f plugins/*/debian/*.substvars

	rm -f shinkenplugins*.tar.xz
	rm -f shinkenplugins*.build
	rm -rf "home:ReAzem:sfl-shinken-plugins"

mrproper: clean
	git submodule foreach git checkout .
