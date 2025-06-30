superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@localhost \
  --password secret && \
superset db upgrade && \
superset init && \
python <<EOF
from superset import security_manager
from superset.models.core import User
from flask_appbuilder.security.sqla.models import Role
from superset.extensions import db

admin_user = db.session.query(User).filter_by(username='admin').first()
admin_role = db.session.query(Role).filter_by(name='Admin').first()

if admin_role not in admin_user.roles:
    admin_user.roles.append(admin_role)
    db.session.commit()
EOF

/usr/bin/run-server.sh
