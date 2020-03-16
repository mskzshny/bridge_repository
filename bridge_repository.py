# pip3 install GitPython
import git
import os
import shutil
from distutils.dir_util import copy_tree

# コピー元のリポジトリ情報
src_repo_url = 'git@github.com:mskzshny/ppt_trim.git'
src_repo_dir = 'src_repo'
src_repo_commit_log_branch = 'master'
src_repo_commit_log_count = 2

# コピー先のリポジトリ情報
dest_repo_url = 'git@github.com:mskzshny/dest_git_repository.git'
dest_repo_dir = 'dest_repo'
dest_repo_commit_log_branch = 'master'

try:
    # コピー元の.gitディレクトリの削除
    shutil.rmtree('./' + src_repo_dir)
except FileNotFoundError:
    print('FileNotFoundError')

try:
    # コピー先の.gitディレクトリの削除
    shutil.rmtree('./' + dest_repo_dir)
except FileNotFoundError:
    print('FileNotFoundError')

# コピー元のGITリポジトリをCLONE
src_repo = git.Repo.clone_from(src_repo_url, src_repo_dir)

# コピー先のGITリポジトリをCLONE
dest_repo = git.Repo.clone_from(dest_repo_url, dest_repo_dir)

# コピー元のリポジトリログの取得
src_log = ""
for item in src_repo.iter_commits(src_repo_commit_log_branch, max_count=src_repo_commit_log_count):
    src_log += item.message

print("src_log : {}".format(src_log))

# コピー元の.gitディレクトリの削除
shutil.rmtree('./'+ src_repo_dir + '/.git')

# ファイルのコピー
copy_tree('./'+src_repo_dir, './'+ dest_repo_dir)

# コピー先へのコミット
dest_repo.git.add(['.'])
dest_repo.git.commit('.','-m',src_log)

# コミットコメントの確認
for item in dest_repo.iter_commits(dest_repo_commit_log_branch, max_count=2):
    print( "dest_repo : {}".format(item.message) )

# コピー先へのPUSH
origin = dest_repo.remote(name='origin')
origin.push(dest_repo_commit_log_branch)