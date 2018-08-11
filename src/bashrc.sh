

function semantic-csharp()
{
    current_dir=$PWD

    cd $SEMANTIC_CODE_DIR
    python2 tool/semantic_csharp.py $current_dir $1 $2

    cd $current_dir
}

function semantic-yaml()
{
    current_dir=$PWD

    file_path=$(abspath $1)

    cd $SEMANTIC_CODE_DIR
    python3 tool/semantic_yaml.py $file_path $2

    cd $current_dir
}