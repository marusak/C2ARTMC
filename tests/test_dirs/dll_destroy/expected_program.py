# pointer variables are : next=5, pn=2, pt=1, v0=3
# next pointers are : l=0, r=1
# data values are : 
def get_program():
    program=[
        ("new","00000000",1,1,"NOABSTR"),
        ("x.next=null","00000001",1,0,2,"NOABSTR"),
        ("x.next=null","00000010",1,1,3,"NOABSTR"),
        ("if*","00000011",4,17),
        ("x=y","00000100",2,1,5,"NOABSTR"),
        ("if*","00000101",6,10,"NOABSTR"),
        ("ifx==null","00000110",2,9,7),
        ("x=y.next","00000111",2,2,0,8,"NOABSTR"),
        ("goto","00001000",6,"NOABSTR"),
        ("goto","00001001",13,"NOABSTR"),
        ("ifx==null","00001010",2,13,11),
        ("x=y.next","00001011",2,2,1,12,"NOABSTR"),
        ("goto","00001100",10,"NOABSTR"),
        ("new","00001101",2,14,"NOABSTR"),
        ("x.next=null","00001110",2,0,15,"NOABSTR"),
        ("x.next=null","00001111",2,1,16,"NOABSTR"),
        ("goto","00010000",3,"NOABSTR"),
        ("x=y.next","00010001",3,1,0,18),
        ("ifx==null","00010010",3,23,19,"NOABSTR"),
        ("x=y.next","00010011",3,1,0,20,"NOABSTR"),
        ("x=y.next","00010100",4,3,0,21,"NOABSTR"),
        ("x.next=y","00010101",1,4,0,22,3,"NOABSTR"),
        ("goto","00010110",17,"NOABSTR"),
        ("x=y.next","00010111",3,1,1,24),
        ("ifx==null","00011000",3,29,25,"NOABSTR"),
        ("x=y.next","00011001",3,1,1,26,"NOABSTR"),
        ("x=y.next","00011010",5,3,1,27,"NOABSTR"),
        ("x.next=y","00011011",1,5,1,28,4,"NOABSTR"),
        ("goto","00011100",23,"NOABSTR"),
        ("goto","00011101",30,"NOABSTR"),
        ("exit","00011110","NOABSTR")]
    node_width=20
    pointer_num=5
    desc_num=5
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)