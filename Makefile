tests:
	tools/run-tests.sh

deb: clean
	tools/update-deb.sh

update-submodules:
	tools/update-submodules.sh

obs:
	tools/update-obs-packages.sh

clean:
	rm -f *.debian.tar.gz
	rm -f *.orig.tar.gz
	rm -f *.dsc
	rm -f *source.changes
	rm -rf "home:ReAzem:sfl-shinken-plugins"

mrproper: clean
	git submodule foreach git checkout .
