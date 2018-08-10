

function semantic-csharp()
{
    current_dir=$PWD

    cd $SEMANTIC_CODE_DIR
    python2 tool/semantic_csharp.py $current_dir $1 $2

    cd $current_dir
}