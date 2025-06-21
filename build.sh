# #!/usr/bin/env bash

# set -o errexit


# pip install -r requirements.txt

# python manage.py collectstatic --no-input
# python manage.py migrate

#!/usr/bin/env bash

# أوقف السكريبت لو فيه أي خطأ
set -o errexit

# تثبيت المتطلبات
pip install --upgrade pip
pip install -r requirements.txt

# ترحيل قاعدة البيانات
python manage.py migrate

# جمع ملفات static
python manage.py collectstatic --no-input
