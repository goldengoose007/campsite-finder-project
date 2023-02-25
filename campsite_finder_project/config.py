class Config:
    def __init__(self, env, emulation):

        # Test emulation
        supported_emulations = ['mobile', 'desktop']
        if emulation.lower() not in supported_emulations:
            raise Exception(f'{emulation} is not a supported environment (Supported emulations: {supported_emulations})')

        # Test env, dev, prod, stage...
        supported_envs = ['dev', 'prod', 'stage', 'uat', 'review-app']

        if env.lower() not in supported_envs:
            raise Exception(f'{env} is not a supported envirnment (supported envs: {supported_envs})')

        self.env = env
        self.emulation = emulation

        self.base_url_riverside_campground = {
            'dev': '',
            'stage': '',
            'prod': 'https://www.riversidecampground.com/'
        }[env]

