import urllib, http.cookiejar
import requests

from html.parser import HTMLParser
from html.entities import name2codepoint
import lxml.html
import getpass
'''
my ($self) = @_;
    my $r = $self->_get("https://accgle.comounts.goo/ServiceLogin");
    $r->content =~ m/GALX.*?value=\"(.*?)\"\>/gms ;
    $self->{galx} = $1;

    $r = $self->_post("https://accounts.google.com/ServiceLoginAuth",
        [
            GALX             => $self->{galx},
            Email            => $self->{login},
            Passwd           => $self->{pass},
            PersistentCookie => 'yes',
            bgresponse       => 'js_disabled',
            continue         => 'https://translate.google.com'
        ]
    );

    $r->content =~ /href=\"(.*)\"/gmsi;
    my $redirect = $1;
    # confirm login
    $self->_get($redirect);
    return $self;
}
sub get_key {
    my ($self) = @_;
    $self->{browser}->agent('Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36');
    my $r = $self->_get('https://translate.google.com');
    $r->content =~ /USAGE\='(.+?)'/gmsi;
    $self->{google_key} = $1;
    return $self;
}

# phrasebook as json blob
sub get_pb {
    my ($self) = @_;
    my $r = $self->_post('https://translate.google.com/translate_a/sg?client=t&cm=g&hl=en&xt=' . $self->{google_key})->content;
    $r =~ s/,,/,"",/gms; # json fix?
    return decode_json($r);
}



'''

def test_login(user, passwd):
    url = "https://accounts.google.com/ServiceLogin"
    jar = requests.cookies.RequestsCookieJar()
    ses = requests.session()
    login_html = ses.get(url, cookies=jar)
    if (login_html.status_code != 200):
        print(" Can not access Google Services. Status Code ", login_html.status_code)
        exit()
    doc = lxml.html.fromstring(login_html.content)
    my_dict = {}
    for form in doc.forms:
        for input in form.inputs:
            #print ('%s: %s' % (input.name, input.value) )
            my_dict[input.name] = input.value
    my_dict['Email'] = user
    my_dict['Passwd'] = passwd
    my_dict['continue'] = 'https://translate.google.com'
    post_r = ses.post('https://accounts.google.com/ServiceLoginAuth', cookies=login_html.cookies, data=my_dict)
    if (post_r.status_code != 200):
        print(" Can not login to the Google Account . Status Code ", post_r.status_code)
        exit()
    ids = post_r.text.find("USAGE")
    ids = post_r.text.find('=',ids)+2
    ide = post_r.text.find(';', ids)-1
    key = post_r.text[ids:ide]
    print( "Google key is: ", key)

    pb_r = ses.post('https://translate.google.com/translate_a/sg?client=t&cm=g&hl=en&xt='+key, cookies=post_r.cookies)
    if ( pb_r.status_code != 200 ):
        print(  " Can not retrieve the phrase book . Status Code ", pb_r.status_code )
        exit()

    jsn = pb_r.json()
    num = jsn[0]
    print("==============================")
    print("Number of translations: ", num)
    for l in jsn[2]:
        print(*l, sep=',')
    print("Done")



if __name__ == '__main__':
    #user = input("Please enter User Email: ")
    #pwd = getpass.getpass("Please enter Password: ")
    user="igor.polevoy@gmail.com"
    pwd="baklan@334"
    test_login(user , pwd)