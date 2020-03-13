# pip3 install GitPython
import git
import os
import shutil
from distutils.dir_util import copy_tree

try:
    # コピー元の.gitディレクトリの削除
    shutil.rmtree('./src_repo')
except FileNotFoundError:
    print('FileNotFoundError')

try:
    # コピー元の.gitディレクトリの削除
    shutil.rmtree('./dest_repo')
except FileNotFoundError:
    print('FileNotFoundError')

# コピー元のGITリポジトリをCLONE
src_repo = git.Repo.clone_from('git@github.com:mskzshny/ppt_trim.git', 'src_repo')

# コピー先のGITリポジトリをCLONE
dest_repo = git.Repo.clone_from('git@github.com:mskzshny/dest_git_repository.git', 'dest_repo')

# コピー元のリポジトリログの取得
src_log = ""
for item in src_repo.iter_commits('master', max_count=2):
    src_log += item.message

print("src_log : {}".format(src_log))

# コピー元の.gitディレクトリの削除
shutil.rmtree('./src_repo/.git')

# ファイルのコピー
copy_tree('./src_repo/', './dest_repo/')

# コピー先へのコミット
dest_repo.git.add(['.'])
dest_repo.git.commit('.','-m',src_log)

# コミットコメントの確認
for item in dest_repo.iter_commits('master', max_count=2):
    print( "dest_repo : {}".format(item.message) )

# コピー先へのPUSH
origin = dest_repo.remote(name='origin')
origin.push('master')