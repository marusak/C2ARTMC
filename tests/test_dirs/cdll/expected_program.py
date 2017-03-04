# pointer variables are : tmp=1, v0=4, x=2, y=3, z=5
# next pointers are : next=0, prev=1
# data values are : 0="00000001"
def get_program():
    program=[
        ("x=null","00000000",2,1),
        ("x=null","00000001",3,2),
        ("new","00000010",2,3),
        ("x.next=y","00000011",2,2,0,4,3),
        ("x.next=y","00000100",2,2,1,5,4),
        ("setdata","00000101",2,"00000001",6),
        ("if*","00000110",7,16),
        ("new","00000111",3,8),
        ("x=y.next","00001000",4,2,0,9),
        ("x.next=y","00001001",3,4,0,10,5),
        ("x=y.next","00001010",1,3,0,11),
        ("x.next=y","00001011",3,2,1,12,6),
        ("setdata","00001100",3,"00000001",13),
        ("x.next=y","00001101",2,3,0,14,7),
        ("x=null","00001110",3,15),
        ("goto","00001111",6),
        ("x=y.next","00010000",3,2,0,17),
        ("ifx==y","00010001",3,2,21,18),
        ("x=y","00010010",5,3,19),
        ("x=y.next","00010011",3,3,0,20),
        ("goto","00010100",17),
        ("goto","00010101",22),
        ("exit","00010110")]
    node_width=24
    pointer_num=6
    desc_num=8
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)