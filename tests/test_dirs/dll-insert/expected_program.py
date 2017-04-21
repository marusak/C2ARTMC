# pointer variables are : v0=4, v1=5, v2=6, x=1, y=2, z=3
# next pointers are : next=0, prev=1
# data values are : 0="00000001"
def get_program():
    program=[
        ("x=null","00000000",1,1,"NOABSTR"),
        ("x=null","00000001",2,2,"NOABSTR"),
        ("if*","00000010",3,12),
        ("new","00000011",2,4,"NOABSTR"),
        ("x.next=y","00000100",2,1,0,5,3,"NOABSTR"),
        ("x.next=null","00000101",2,1,6,"NOABSTR"),
        ("setdata","00000110",2,"00000001",7,"NOABSTR"),
        ("ifx==null","00000111",1,10,8,"NOABSTR"),
        ("x.next=y","00001000",1,2,1,9,4,"NOABSTR"),
        ("goto","00001001",10,"NOABSTR"),
        ("x=y","00001010",1,2,11,"NOABSTR"),
        ("goto","00001011",2,"NOABSTR"),
        ("x=y","00001100",2,1,13,"NOABSTR"),
        ("ifx==null","00001101",2,29,14),
        ("if*","00001110",15,27,"NOABSTR"),
        ("new","00001111",3,16,"NOABSTR"),
        ("x=y.next","00010000",4,2,0,17,"NOABSTR"),
        ("x.next=y","00010001",3,4,0,18,5,"NOABSTR"),
        ("x.next=y","00010010",3,2,1,19,6,"NOABSTR"),
        ("x.next=y","00010011",2,3,0,20,7,"NOABSTR"),
        ("x=y.next","00010100",5,3,0,21,"NOABSTR"),
        ("ifx==null","00010101",5,25,22,"NOABSTR"),
        ("x=y.next","00010110",6,3,0,23,"NOABSTR"),
        ("x.next=y","00010111",6,3,1,24,8,"NOABSTR"),
        ("goto","00011000",25,"NOABSTR"),
        ("goto","00011001",29,"NOABSTR"),
        ("goto","00011010",27,"NOABSTR"),
        ("x=y.next","00011011",2,2,0,28,"NOABSTR"),
        ("goto","00011100",13,"NOABSTR"),
        ("ifx==null","00011101",1,33,30),
        ("x=y","00011110",2,1,31,"NOABSTR"),
        ("x=y.next","00011111",1,1,0,32,"NOABSTR"),
        ("goto","00100000",29,"NOABSTR"),
        ("goto","00100001",34,"NOABSTR"),
        ("exit","00100010","NOABSTR")]
    node_width=26
    pointer_num=7
    desc_num=9
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)