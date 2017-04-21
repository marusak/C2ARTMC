# pointer variables are : v0=5, v1=6, v2=7, v3=8, v4=9, v5=10, x=1, y=2, yLast=4, z=3
# next pointers are : next=0, prev=1
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",1,1,"NOABSTR"),
        ("x=null","00000001",2,2,"NOABSTR"),
        ("new","00000010",1,3,"NOABSTR"),
        ("x.next=null","00000011",1,0,4,"NOABSTR"),
        ("x.next=null","00000100",1,1,5,"NOABSTR"),
        ("if*","00000101",6,12),
        ("new","00000110",2,7,"NOABSTR"),
        ("x.next=y","00000111",2,1,0,8,3,"NOABSTR"),
        ("x.next=y","00001000",1,2,1,9,4,"NOABSTR"),
        ("x.next=null","00001001",2,1,10,"NOABSTR"),
        ("x=y","00001010",1,2,11,"NOABSTR"),
        ("goto","00001011",5,"NOABSTR"),
        ("x=null","00001100",3,13,"NOABSTR"),
        ("new","00001101",2,14,"NOABSTR"),
        ("x.next=null","00001110",2,0,15,"NOABSTR"),
        ("x.next=null","00001111",2,1,16,"NOABSTR"),
        ("x=y","00010000",4,2,17,"NOABSTR"),
        ("if*","00010001",18,24),
        ("new","00010010",3,19,"NOABSTR"),
        ("x.next=y","00010011",3,2,0,20,5,"NOABSTR"),
        ("x.next=y","00010100",2,3,1,21,6,"NOABSTR"),
        ("x.next=null","00010101",3,1,22,"NOABSTR"),
        ("x=y","00010110",2,3,23,"NOABSTR"),
        ("goto","00010111",17,"NOABSTR"),
        ("x.next=y","00011000",4,1,0,25,7,"NOABSTR"),
        ("x.next=y","00011001",1,4,1,26,8,"NOABSTR"),
        ("x=null","00011010",2,27,"NOABSTR"),
        ("x=null","00011011",3,28,"NOABSTR"),
        ("x=y","00011100",2,1,29,"NOABSTR"),
        ("ifx==null","00011101",2,32,30),
        ("x=y.next","00011110",2,2,0,31,"NOABSTR"),
        ("goto","00011111",29,"NOABSTR"),
        ("x=y.next","00100000",5,1,0,33),
        ("ifx==null","00100001",5,39,34,"NOABSTR"),
        ("x=y.next","00100010",2,1,0,35,"NOABSTR"),
        ("x=y.next","00100011",6,1,0,36,"NOABSTR"),
        ("x=y.next","00100100",7,6,0,37,"NOABSTR"),
        ("x.next=y","00100101",1,7,0,38,9,"NOABSTR"),
        ("goto","00100110",32,"NOABSTR"),
        ("x=y.next","00100111",8,1,1,40),
        ("ifx==null","00101000",8,46,41,"NOABSTR"),
        ("x=y.next","00101001",2,1,1,42,"NOABSTR"),
        ("x=y.next","00101010",9,1,1,43,"NOABSTR"),
        ("x=y.next","00101011",10,9,1,44,"NOABSTR"),
        ("x.next=y","00101100",1,10,1,45,10,"NOABSTR"),
        ("goto","00101101",39,"NOABSTR"),
        ("goto","00101110",47,"NOABSTR"),
        ("exit","00101111","NOABSTR")]
    node_width=32
    pointer_num=11
    desc_num=11
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)