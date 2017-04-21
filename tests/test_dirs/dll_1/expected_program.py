# pointer variables are : tmp=1, v0=5, x=2, y=3, z=4
# next pointers are : next=0, prev=1
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",2,1,"NOABSTR"),
        ("x=null","00000001",3,2,"NOABSTR"),
        ("x=null","00000010",4,3,"NOABSTR"),
        ("new","00000011",2,4,"NOABSTR"),
        ("x.next=null","00000100",2,0,5,"NOABSTR"),
        ("x.next=null","00000101",2,1,6,"NOABSTR"),
        ("if*","00000110",7,13),
        ("new","00000111",3,8,"NOABSTR"),
        ("x.next=y","00001000",3,2,0,9,3,"NOABSTR"),
        ("x.next=y","00001001",2,3,1,10,4,"NOABSTR"),
        ("x.next=null","00001010",3,1,11,"NOABSTR"),
        ("x=y","00001011",2,3,12,"NOABSTR"),
        ("goto","00001100",6,"NOABSTR"),
        ("if*","00001101",14,27),
        ("x=y","00001110",3,2,15,"NOABSTR"),
        ("x=y.next","00001111",5,3,0,16),
        ("ifx==null","00010000",5,20,17,"NOABSTR"),
        ("if*","00010001",18,20,"NOABSTR"),
        ("x=y.next","00010010",3,3,0,19,"NOABSTR"),
        ("goto","00010011",15,"NOABSTR"),
        ("x=y.next","00010100",5,3,0,21,"NOABSTR"),
        ("ifx==null","00010101",5,26,22,"NOABSTR"),
        ("x=y.next","00010110",1,3,0,23,"NOABSTR"),
        ("x=y.next","00010111",4,1,0,24,"NOABSTR"),
        ("x.next=y","00011000",3,4,0,25,5,"NOABSTR"),
        ("goto","00011001",26,"NOABSTR"),
        ("goto","00011010",13,"NOABSTR"),
        ("x=y.next","00011011",5,2,0,28),
        ("ifx==null","00011100",5,34,29,"NOABSTR"),
        ("x=y.next","00011101",3,2,0,30,"NOABSTR"),
        ("x=y.next","00011110",1,2,0,31,"NOABSTR"),
        ("x=y.next","00011111",5,1,0,32,"NOABSTR"),
        ("x.next=y","00100000",2,5,0,33,6,"NOABSTR"),
        ("goto","00100001",27,"NOABSTR"),
        ("goto","00100010",35,"NOABSTR"),
        ("exit","00100011","NOABSTR")]
    node_width=23
    pointer_num=6
    desc_num=7
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)