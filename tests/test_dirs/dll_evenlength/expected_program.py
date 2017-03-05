# pointer variables are : x=1, y=2
# next pointers are : next=0, prev=1
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",1,1),
        ("x=null","00000001",2,2),
        ("new","00000010",2,3),
        ("x.next=y","00000011",2,1,0,4,3),
        ("x=y","00000100",1,2,5),
        ("new","00000101",2,6),
        ("x.next=y","00000110",2,1,0,7,4),
        ("x.next=y","00000111",1,2,1,8,5),
        ("x=y","00001000",1,2,9),
        ("if*","00001001",10,19),
        ("new","00001010",2,11),
        ("x.next=y","00001011",2,1,0,12,6),
        ("x.next=y","00001100",1,2,1,13,7),
        ("x=y","00001101",1,2,14),
        ("new","00001110",2,15),
        ("x.next=y","00001111",2,1,0,16,8),
        ("x.next=y","00010000",1,2,1,17,9),
        ("x=y","00010001",1,2,18),
        ("goto","00010010",9),
        ("ifx==null","00010011",2,25,20),
        ("x=y","00010100",1,2,21),
        ("x=y.next","00010101",2,2,0,22),
        ("x=y","00010110",1,2,23),
        ("x=y.next","00010111",2,2,0,24),
        ("goto","00011000",19),
        ("goto","00011001",26),
        ("exit","00011010")]
    node_width=23
    pointer_num=3
    desc_num=10
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)