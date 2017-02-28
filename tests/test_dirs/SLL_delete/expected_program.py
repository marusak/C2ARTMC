# pointer variables are : elem=2, prev=3, temp=4, x=1
# next pointers are : next=0
# data values are : delval="00000001"
def get_program():
    program=[
        ("x=y","00000000",2,1,1),
        ("x=null","00000001",3,2),
        ("x=null","00000010",4,3),
        ("ifx==null","00000011",2,16,4),
        ("ifdata","00000100",2,"00000001",5,13),
        ("ifx==null","00000101",3,6,8),
        ("x=y.next","00000110",1,2,0,7),
        ("goto","00000111",10),
        ("x=y.next","00001000",4,2,0,9),
        ("x.next=y","00001001",3,4,0,10,4),
        ("x.next=null","00001010",2,0,11),
        ("goto","00001011",17),
        ("goto","00001100",13),
        ("x=y","00001101",3,2,14),
        ("x=y.next","00001110",2,2,0,15),
        ("goto","00001111",3),
        ("goto","00010000",17),
        ("exit","00010001")]
    node_width=20
    pointer_num=5
    desc_num=5
    next_num=1
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)