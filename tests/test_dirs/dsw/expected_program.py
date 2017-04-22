# pointer variables are : t=3, x=1, y=2
# next pointers are : left=0, right=1
# data values are : 0="00000010", 1="00000011", 2="00000001"
def get_program():
    program=[
        ("x=null","00000000",3,1,"NOABSTR"),
        ("ifx==null","00000001",1,2,4,"NOABSTR"),
        ("goto","00000010",37,"NOABSTR"),
        ("goto","00000011",4,"NOABSTR"),
        ("if*","00000100",5,37),
        ("ifdata","00000101",1,"00000001",6,20,"NOABSTR"),
        ("x=y","00000110",2,1,7,"NOABSTR"),
        ("x=y","00000111",1,3,8,"NOABSTR"),
        ("ifx==null","00001000",1,9,11,"NOABSTR"),
        ("goto","00001001",37,"NOABSTR"),
        ("goto","00001010",11,"NOABSTR"),
        ("ifdata","00001011",1,"00000010",12,16,"NOABSTR"),
        ("x=y.next","00001100",3,1,1,13,"NOABSTR"),
        ("x.next=y","00001101",1,2,1,14,4,"NOABSTR"),
        ("setdata","00001110",1,"00000011",15,"NOABSTR"),
        ("goto","00001111",19,"NOABSTR"),
        ("x=y.next","00010000",3,1,0,17,"NOABSTR"),
        ("x.next=y","00010001",1,2,0,18,5,"NOABSTR"),
        ("setdata","00010010",1,"00000001",19,"NOABSTR"),
        ("goto","00010011",36,"NOABSTR"),
        ("ifdata","00010100",1,"00000011",21,29,"NOABSTR"),
        ("x=y.next","00010101",2,1,0,22,"NOABSTR"),
        ("ifx==null","00010110",2,23,25,"NOABSTR"),
        ("setdata","00010111",1,"00000001",24,"NOABSTR"),
        ("goto","00011000",28,"NOABSTR"),
        ("x.next=y","00011001",1,3,0,26,6,"NOABSTR"),
        ("x=y","00011010",3,1,27,"NOABSTR"),
        ("x=y","00011011",1,2,28,"NOABSTR"),
        ("goto","00011100",36,"NOABSTR"),
        ("x=y.next","00011101",2,1,1,30,"NOABSTR"),
        ("ifx==null","00011110",2,31,33,"NOABSTR"),
        ("setdata","00011111",1,"00000011",32,"NOABSTR"),
        ("goto","00100000",36,"NOABSTR"),
        ("x.next=y","00100001",1,3,1,34,7,"NOABSTR"),
        ("x=y","00100010",3,1,35,"NOABSTR"),
        ("x=y","00100011",1,2,36,"NOABSTR"),
        ("goto","00100100",4,"NOABSTR"),
        ("exit","00100101","NOABSTR")]
    node_width=22
    pointer_num=4
    desc_num=8
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)