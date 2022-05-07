import logging
import sys
import os
import stat
import time
import typing
import datetime
import shutil

SDCARD_PATH: str = "F:/DCIM"
DESTINATION_PATH_ROOT: str = "E:/dashcam_dump"
SLEEP_SECONDS: str = 60 * 60
logging.basicConfig(level="DEBUG")


def test_if_dashcam_card(files) -> bool:
    return True if files == ["1", "2"] else False


def get_files_to_copy(files_to_copy):
    _file_path = "%s/1" % SDCARD_PATH
    files_to_copy.extend(["%s/%s" % (_file_path, x) for x in os.listdir(_file_path)])
    _file_path = "%s/2" % SDCARD_PATH
    files_to_copy.extend(["%s/%s" % (_file_path, x) for x in os.listdir(_file_path)])


def copy_files(files_to_copy):
    _datetime = datetime.datetime.now().isoformat().replace(":", "-")
    _this_dest_dir = "%s/%s" % (DESTINATION_PATH_ROOT, _datetime)
    if files_to_copy:
        os.makedirs(_this_dest_dir, exist_ok=True)
    for _file in files_to_copy:
        _cam_no = _file.rsplit("/", 2)[1]
        _file_shortname_no_ext = _file.rsplit("/", 1)[1].split(".")[0]
        _ext = _file.rsplit("/", 1)[1].split(".")[1]
        # TODO: this below is an estimation and only works on windows presumably
        _is_event = False
        # True if os.stat(_file).st_mode < 33206 else False
        # logging.info("is event") if _is_event else None
        _this_dest_file = "%s/%s_cam%s%s.%s" % (
            _this_dest_dir,
            _file_shortname_no_ext,
            _cam_no,
            "_event" if _is_event else "",
            _ext,
        )
        logging.info("copying file %s to %s", _file, _this_dest_file)
        os.chmod(_file, stat.S_IREAD)
        shutil.copyfile(_file, _this_dest_file)
        # if _is_event:
        #     logging.info("marking file read write")
        os.chmod(_file, stat.S_IWRITE)
        os.unlink(_file)


def run():
    files = os.listdir(SDCARD_PATH)
    logging.info("files are %s", repr(files))
    files_to_copy = []
    if test_if_dashcam_card(files):
        get_files_to_copy(files_to_copy)
    copy_files(files_to_copy)


def loop():
    while True:
        if os.path.exists(SDCARD_PATH):
            run()
        time.sleep(SLEEP_SECONDS)


def main(argv):
    try:
        loop()
    except (KeyboardInterrupt, SystemExit) as e:
        logging.info("shutdown gracefully with exception %s", repr(e))
        return 0
    except Exception as e:
        logging.exception("shutdown ungracefully with exception %s", repr(e))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
