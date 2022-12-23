import pyrogram
import sys
import os
for path in sys.path:
   if os.path.exists(os.path.join(path, 'pyrogram')):
      print('pyrogram is here: {}'.format(path))