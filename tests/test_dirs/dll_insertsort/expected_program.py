# pointer variables are : pred=4, sorted=3, x=1, y=2, z=5
# next pointers are : next=0, prev=1
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",1,1,"NOABSTR"),
        ("x=null","00000001",2,2,"NOABSTR"),
        ("if*","00000010",3,11),
        ("new","00000011",2,4,"NOABSTR"),
        ("x.next=y","00000100",2,1,0,5,3,"NOABSTR"),
        ("x.next=null","00000101",2,1,6,"NOABSTR"),
        ("ifx==null","00000110",1,9,7,"NOABSTR"),
        ("x.next=y","00000111",1,2,1,8,4,"NOABSTR"),
        ("goto","00001000",9,"NOABSTR"),
        ("x=y","00001001",1,2,10,"NOABSTR"),
        ("goto","00001010",2,"NOABSTR"),
        ("x=null","00001011",3,12,"NOABSTR"),
        ("x=null","00001100",4,13,"NOABSTR"),
        ("x=null","00001101",5,14,"NOABSTR"),
        ("ifx==null","00001110",1,34,15),
        ("x=y","00001111",2,1,16,"NOABSTR"),
        ("x=y.next","00010000",1,1,0,17,"NOABSTR"),
        ("x=y","00010001",5,3,18,"NOABSTR"),
        ("x=null","00010010",4,19,"NOABSTR"),
        ("ifx==null","00010011",5,24,20),
        ("if*","00010100",21,24,"NOABSTR"),
        ("x=y","00010101",4,5,22,"NOABSTR"),
        ("x=y.next","00010110",5,5,0,23,"NOABSTR"),
        ("goto","00010111",19,"NOABSTR"),
        ("x.next=y","00011000",2,5,0,25,5,"NOABSTR"),
        ("ifx==null","00011001",5,28,26,"NOABSTR"),
        ("x.next=y","00011010",5,2,1,27,6,"NOABSTR"),
        ("goto","00011011",28,"NOABSTR"),
        ("x.next=y","00011100",2,4,1,29,7,"NOABSTR"),
        ("ifx==null","00011101",4,32,30,"NOABSTR"),
        ("x.next=y","00011110",4,2,0,31,8,"NOABSTR"),
        ("goto","00011111",33,"NOABSTR"),
        ("x=y","00100000",3,2,33,"NOABSTR"),
        ("goto","00100001",14,"NOABSTR"),
        ("ifx==null","00100010",3,38,35),
        ("x=y","00100011",2,3,36,"NOABSTR"),
        ("x=y.next","00100100",3,3,0,37,"NOABSTR"),
        ("goto","00100101",34,"NOABSTR"),
        ("goto","00100110",39,"NOABSTR"),
        ("exit","00100111","NOABSTR")]
    node_width=25
    pointer_num=6
    desc_num=9
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)