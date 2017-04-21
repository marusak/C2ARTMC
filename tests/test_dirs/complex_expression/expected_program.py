# pointer variables are : v0=4, v1=5, v2=6, v3=7, v4=8, x=1, y=2, z=3
# next pointers are : left=0, parrent=2, right=1
# data values are : 0="00000001"
def get_program():
    program=[
        ("ifx==null","00000000",1,5,1),
        ("ifx==null","00000001",2,5,2,"NOABSTR"),
        ("x=y.next","00000010",4,1,1,3,"NOABSTR"),
        ("x=y.next","00000011",5,2,1,4,"NOABSTR"),
        ("ifx==y","00000100",4,5,5,10,"NOABSTR"),
        ("x=y.next","00000101",4,2,1,6,"NOABSTR"),
        ("x=y.next","00000110",5,3,1,7,"NOABSTR"),
        ("x=y.next","00000111",6,5,1,8,"NOABSTR"),
        ("x=y.next","00001000",7,6,1,9,"NOABSTR"),
        ("ifx==y","00001001",4,7,23,10,"NOABSTR"),
        ("ifx==null","00001010",1,18,11),
        ("ifx==null","00001011",2,18,12,"NOABSTR"),
        ("x=y.next","00001100",4,1,1,13,"NOABSTR"),
        ("x=y.next","00001101",5,4,1,14,"NOABSTR"),
        ("x=y.next","00001110",6,5,2,15,"NOABSTR"),
        ("x=y.next","00001111",7,2,2,16,"NOABSTR"),
        ("x=y.next","00010000",8,7,0,17,"NOABSTR"),
        ("ifx==y","00010001",6,8,22,18,"NOABSTR"),
        ("x=y.next","00010010",4,2,1,19,"NOABSTR"),
        ("ifdata","00010011",4,"00000001",22,20,"NOABSTR"),
        ("x=y.next","00010100",2,1,1,21,"NOABSTR"),
        ("goto","00010101",10,"NOABSTR"),
        ("goto","00010110",0,"NOABSTR"),
        ("exit","00010111","NOABSTR")]
    node_width=26
    pointer_num=9
    desc_num=7
    next_num=3
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)