import os
import sys


def _apply_data_project_flag(argv):
    """`--data-project <tên>` phải có hiệu lực trước khi các module đọc đường dẫn lúc import."""
    for i, arg in enumerate(argv):
        if arg == "--data-project" and i + 1 < len(argv):
            os.environ["GOBI_PROJECT"] = argv[i + 1]
        elif arg.startswith("--data-project="):
            os.environ["GOBI_PROJECT"] = arg.split("=", 1)[1]


_apply_data_project_flag(sys.argv[1:])

from gobi.cli.main import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
