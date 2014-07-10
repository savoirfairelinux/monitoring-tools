deb:
	tools/update_obs_packages.sh

update-submodules:
	tools/update-submodules.sh

osc:
	tools/update-osc.sh

clean:
	rm *.debian.tar.gz
	rm *.orig.tar.gz
	rm *.dsc
	rm *source.changes
	git submodule foreach git checkout .
