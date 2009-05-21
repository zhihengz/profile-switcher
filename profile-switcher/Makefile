ETC_BASE=etc
BIN_BASE=usr/local/bin

all:	test-list test-status test-switch

test: src/switcher.py conf/profile-switch.conf.xml	
	cp conf/test.conf.xml test/profile-switch.conf
	cp src/switcher.py test/switcher
	chmod +x test/switcher

test-list: test
	cd test && ./switcher --list
test-status: test
	cd test && ./switcher --status
test-switch: test
	rm -fr /home/zhihengz/tmp/test
	ln -s /home/zhihengz/tmp/test1 /home/zhihengz/tmp/test
	cd test && ./switcher --switch test test2
clean:
	rm -fr test
	rm -fr /home/zhihengz/tmp/test
	rm -fr /home/zhihengz/tmp/test1
	rm -fr /home/zhihengz/tmp/test2
	mkdir -p test
	mkdir -p /home/zhihengz/tmp/test1
	mkdir -p /home/zhihengz/tmp/test2
install:

	sed "s/profile-switch.conf/\/etc\/profile-switch.conf/g" src/switcher.py >switcher
	install -m 755 switcher $(DESTDIR)/$(BIN_BASE)
	install -m 644 conf/profile-switch.conf.xml $(DESTDIR)/$(ETC_BASE)/profile-switch.conf.sample
