import hashlib
import base62
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from model.shortUrlModel import ShortUrlOnly, UrlInput, ShortUrl, ShortUrlViews
from database import get_session
from crud import shortUrlCrud
from main import get_session


router = APIRouter(
    dependencies=[Depends(get_session)]
)


@router.post('/shorten', response_model=ShortUrlOnly)
def create_short_url(origin_url: UrlInput, request: Request, session: Session = Depends(get_session)):
    '''
    사용자로부터 url과 expiration_hour를 받아 short_url을 반환해주는 함수입니다.
    '''
    db_short_url = shortUrlCrud.get_short_url_by_url(session, origin_url.url)

    host = request.headers.get('host')
    if db_short_url:
        # 해당 key가 만료되었다면 기간을 업데이트 합니다. 조회수 또한 함께 초기화 합니다.
        if db_short_url.expiration_date < datetime.now():
            expiration_date = datetime.now() + timedelta(hours=min(max(24, origin_url.expiration_hour), 24 * 365))
            shortUrlCrud.update_short_url(session, db_short_url.short_key, expiration_date)
        short_url = f'http://{host}/{db_short_url.short_key}'
        content = {
            'short_url': short_url
        }        
    else:
        hashing_count = 0
        # 짧은 hash값으로 인해 중복된 hash값이 생성될 수 있습니다.
        # 해당 문제를 위해 최대 5번의 해시값 생성을 시도하도록 했습니다.
        while hashing_count < 5:
            current_datetime = datetime.now()
            sha = hashlib.sha256()
            # 같은 url이더라도 매번 다른 해시값이 생성되도록 함으로써 보안성을 높였습니다.
            sha.update(f'{current_datetime}{origin_url.url}'.encode('utf-8'))
            # 짧은 key를 반환하기 위해 62진수로 변환 후 앞에서 10자리의 값만 사용했습니다.
            hashed_key = base62.encodebytes(sha.digest())[:10]
            db_short_url_by_key = shortUrlCrud.get_short_url_by_short_key(session, hashed_key)
            if db_short_url_by_key:
                hashing_count += 1
            else:
                new_short_url = ShortUrl(
                    url = origin_url.url,
                    expiration_date = datetime.now() + timedelta(hours=min(max(24, origin_url.expiration_hour), 24 * 365)),
                    short_key = hashed_key
                )
                shortUrlCrud.create_short_url(session, new_short_url)
                short_url = f'http://{host}/{hashed_key}'
                content = {
                    'short_url': short_url
                }
                break
        # 5번의 중복 해시값을 생성하면 다시 시도해달라는 문구를 보내도록 했습니다.
        if hashing_count == 5:
            raise HTTPException(status_code=400, detail='retry please')
    return content

@router.get('/{short_key}')
def redirect_short_url(short_key: str, session: Session = Depends(get_session)):
    db_short_url = shortUrlCrud.get_short_url_by_short_key(session, short_key)
    if db_short_url:
        #만료된 url의 경우 리다이렉트 하지 않고 데이터 삭제 처리를 했습니다.
        if db_short_url.expiration_date > datetime.now():
            shortUrlCrud.update_short_url_views(session, short_key)
            return RedirectResponse(url=db_short_url.url, status_code=301)
        shortUrlCrud.delete_short_url(session, short_key)
    raise HTTPException(status_code=404, detail='there is no shorturl')

@router.get('/stat/{short_key}')
def get_short_url_views(short_key: str, session: Session = Depends(get_session)):
    db_short_url = shortUrlCrud.get_short_url_by_short_key(session, short_key)
    if db_short_url:
        content = {
            'short_key': db_short_url.short_key,
            'views': db_short_url.views
        }
        return content
    raise HTTPException(status_code=404, detail='there is no shorturl')