# pointer variables are : x=1, y=2
# next pointers are : left=0, parrent=2, right=1
# data values are : 0="00000001", 1="00000010"
def get_program():
    program=[
        ("ifx==null","00000000",1,14,1),
        ("x=y.next","00000001",2,1,0,2,"NOABSTR"),
        ("ifx==null","00000010",2,6,3,"NOABSTR"),
        ("ifdata","00000011",2,"00000001",4,6,"NOABSTR"),
        ("x=y","00000100",1,2,5,"NOABSTR"),
        ("goto","00000101",13,"NOABSTR"),
        ("x=y.next","00000110",2,1,1,7,"NOABSTR"),
        ("ifx==null","00000111",2,11,8,"NOABSTR"),
        ("ifdata","00001000",2,"00000001",9,11,"NOABSTR"),
        ("x=y","00001001",1,2,10,"NOABSTR"),
        ("goto","00001010",13,"NOABSTR"),
        ("setdata","00001011",1,"00000010",12,"NOABSTR"),
        ("x=y.next","00001100",1,1,2,13,"NOABSTR"),
        ("goto","00001101",0,"NOABSTR"),
        ("exit","00001110","NOABSTR")]
    node_width=20
    pointer_num=3
    desc_num=7
    next_num=3
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)