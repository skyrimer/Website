from subprocess import call
call('git init')
call("git add -A")
call('git commit -m "commit for git"')
call("git remote add origin https://github.com/skyrimer/Website")
call("git push -u origin master")