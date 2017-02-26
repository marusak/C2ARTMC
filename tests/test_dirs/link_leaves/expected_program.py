# pointer variables are : q=3, x=4, y=1, z=2
# next pointers are : left=0, parrent=2, right=1, successor=3
# data values are : 
def get_program():
    program=[
        ("x=y.next","00000000",1,4,0,1),
        ("ifx==null","00000001",1,5,2),
        ("x=y","00000010",4,1,3),
        ("x=y.next","00000011",1,4,0,4),
        ("goto","00000100",1),
        ("x=y","00000101",3,4,6),
        ("x=y.next","00000110",1,3,2,7),
        ("ifx==null","00000111",1,22,8),
        ("x=y.next","00001000",2,1,1,9),
        ("ifx==y","00001001",2,1,10,12),
        ("x=y","00001010",3,1,11),
        ("goto","00001011",20),
        ("x=y.next","00001100",3,1,1,13),
        ("x=y.next","00001101",1,3,0,14),
        ("ifx==null","00001110",1,18,15),
        ("x=y","00001111",3,1,16),
        ("x=y.next","00010000",1,3,0,17),
        ("goto","00010001",14),
        ("x.next=y","00010010",4,3,3,19,5),
        ("x=y","00010011",4,3,20),
        ("x=y.next","00010100",1,3,2,21),
        ("goto","00010101",7),
        ("exit","00010110")]
    node_width=21
    pointer_num=5
    desc_num=6
    next_num=4
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)